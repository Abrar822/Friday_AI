
use std::fs::OpenOptions;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::thread;
use std::time::{Duration, Instant};
use std::os::windows::process::CommandExt;

use tauri::{Manager, RunEvent, path::BaseDirectory};

struct BackendState {
    child: Mutex<Option<Child>>,
    url: String,
}

#[tauri::command]
fn get_backend_url(state: tauri::State<'_, BackendState>) -> String {
    state.url.clone()
}

fn find_free_port() -> std::io::Result<u16> {
    let listener = TcpListener::bind(("127.0.0.1", 0))?;
    let port = listener.local_addr()?.port();
    drop(listener);
    Ok(port)
}

fn wait_for_backend(
    port: u16,
    child: &mut Child,
) -> Result<(), Box<dyn std::error::Error>> {
    let deadline = Instant::now() + Duration::from_secs(300);
    let address = format!("127.0.0.1:{port}").parse()?;

    while Instant::now() < deadline {
        if let Some(status) = child.try_wait()? {
            return Err(format!(
                "Friday backend exited before becoming ready: {status}"
            ).into());
        }

        if let Ok(mut stream) =
            TcpStream::connect_timeout(&address, Duration::from_millis(300))
        {
            stream.set_read_timeout(Some(Duration::from_secs(2)))?;

            stream.write_all(
                b"GET /health HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n",
            )?;

            let mut response = [0_u8; 1024];

            if let Ok(count) = stream.read(&mut response) {
                let response = String::from_utf8_lossy(&response[..count]);

                if response.starts_with("HTTP/1.1 200")
                    || response.starts_with("HTTP/1.0 200")
                {
                    return Ok(());
                }
            }
        }

        thread::sleep(Duration::from_millis(250));
    }

    let _ = child.kill();
    let _ = child.wait();

    Err("Friday backend did not become ready within 300 seconds".into())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let app = tauri::Builder::default()
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![get_backend_url])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;

                // Development: use the Python backend started by dev.py.
                let backend_url = std::env::var("VITE_BACKEND_URL")
                    .map_err(|_| {
                        std::io::Error::new(
                            std::io::ErrorKind::NotFound,
                            "VITE_BACKEND_URL is missing. Start using backend/dev.py.",
                        )
                    })?;

                app.manage(BackendState {
                    child: Mutex::new(None),
                    url: backend_url,
                });

                return Ok(());
            }

            // Production: start the packaged backend.
            let backend_exe = app.path().resolve(
                "FridayBackend/FridayBackend.exe",
                BaseDirectory::Resource,
            )?;

            if !backend_exe.exists() {
                return Err(format!(
                    "Packaged backend executable not found: {}",
                    backend_exe.display()
                ).into());
            }

            let resource_dir = app.path().resource_dir()?;
            let port = find_free_port()?;

            let log_dir = app.path().app_log_dir()?;
            std::fs::create_dir_all(&log_dir)?;

            let log_file = OpenOptions::new()
                .create(true)
                .append(true)
                .open(log_dir.join("backend.log"))?;

            let error_file = log_file.try_clone()?;

            let mut command = Command::new(&backend_exe);
            command
                .arg("--port")
                .arg(port.to_string())
                .current_dir(&resource_dir)
                .stdin(Stdio::null())
                .stdout(Stdio::from(log_file))
                .stderr(Stdio::from(error_file))
                .creation_flags(0x08000000);

            let mut child = command.spawn()?;

            if let Err(error) = wait_for_backend(port, &mut child) {
                let _ = child.kill();
                let _ = child.wait();
                return Err(error);
            }

            app.manage(BackendState {
                child: Mutex::new(Some(child)),
                url: format!("http://127.0.0.1:{port}"),
            });

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("Failed to build Friday");

    app.run(|handle, event| {
        if let RunEvent::Exit = event {
            if let Some(state) = handle.try_state::<BackendState>() {
                if let Ok(mut child) = state.child.lock() {
                    if let Some(child) = child.as_mut() {
                        let _ = child.kill();
                        let _ = child.wait();
                    }
                }
            }
        }
    });
}
