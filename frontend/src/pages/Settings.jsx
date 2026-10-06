import { settingConnect, fetchSetting } from "../helper/setting_api";

export default function Settings({ setting, setSetting, setAlert }) {
  return (
    <>
      <div className="setting-container max-w-[830px] min-w-[500px] w-full bg-(--sidebar-bg) text-(--text-primary) border-solid border-[1px] border-(--dark-border) ml-[90px] mt-[70px] px-[15px] py-[10px] rounded-xl flex flex-col justify-start items-center gap-6">
        <div className="name w-full flex gap-8 justify-start items-center">
          <div className="w-[100px]">Name</div>
          <input
            type="text"
            className="text-black bg-(--text-primary) border-[1px] border-solid border-(--dark-border) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 transition-all duration-250 ease-in"
            placeholder="Enter your name"
            onChange={(e) => {
              setSetting((prev) => ({ ...prev, name: e.target.value }));
            }}
            value={setting.name}
          />
        </div>
        <div className="name w-full flex gap-8 justify-start items-center">
          <div className="w-[100px]">Groq Api Key</div>
          <input
            type="text"
            className="text-black bg-(--text-primary) border-[1px] border-solid border-(--dark-border) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 transition-all duration-250 ease-in"
            placeholder="Enter your Api Key"
            onChange={(e) => {
              setSetting((prev) => ({ ...prev, api_key: e.target.value }));
            }}
            value={setting.api_key}
          />
        </div>
        <div className="name w-full flex gap-8 justify-start items-center">
          <div className="w-[100px]">Llm Mode</div>
          <div className="flex w-[150px] gap-4 items-center justify-center">
            <button
              type="text"
              className={`text-(--text-primary) bg-(--sidebar-bg) border-[1px] border-solid border-(--dark-border) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 cursor-pointer`}
              placeholder="Enter your Mode"
              onClick={(e) => {
                setSetting((prev) => ({ ...prev, llm_mode: setting.llm_mode === 'groq' ? 'qwen': 'groq' }));
              }}
              value={setting.llm_mode}
            >
              {setting.llm_mode === 'groq'? <span>Groq</span> : <span>Local</span>}
            </button>
          </div>
        </div>
        <button
          className="save self-start bg-[linear-gradient(135deg,#b06bff,#5b8bff)] rounded-lg h-[40] px-[10px] py-[5px] cursor-pointer transition-all active:scale-95 duration-250 ease-in"
          onClick={async () => {
            try {
              let response = await settingConnect(setting);
              if (response.message) {
                setAlert({ msg: response.message, state: true });
                let data = await fetchSetting();
                console.log("received: ", data);
                setSetting({
                  name: data.name,
                  api_key: data.api_key,
                  llm_mode: data.llm_mode,
                });
              }
            } catch (err) {
              setAlert({ msg: err.message, state: true });
            }
          }}
        >
          Save Changes
        </button>
      </div>
    </>
  );
}
