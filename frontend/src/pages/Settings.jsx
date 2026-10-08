import { settingConnect, fetchSetting } from "../helper/setting_api";
import { useState } from "react";

export default function Settings({ setting, setSetting, setAlert }) {
  const [eye, setEye] = useState(true);
  return (
    <>
      <div className="setting-container max-w-[830px] min-w-[500px] w-full bg-(--sidebar-bg) text-(--text-primary) border-solid border-[1px] border-(--dark-border) ml-[90px] mt-[70px] px-[15px] py-[10px] rounded-xl flex flex-col justify-start items-center gap-6">
        <div className="name w-full flex gap-8 justify-start items-center">
          <div className="w-[100px]">Name</div>
          <input
            type="text"
            className="text-(--text-primary) bg-(--message) border-[1px] border-solid border-(--dark-border) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 transition-all duration-250 ease-in"
            placeholder="Enter your name"
            onChange={(e) => {
              setSetting((prev) => ({ ...prev, name: e.target.value }));
            }}
            value={setting.name}
          />
        </div>
        <div className="name w-full flex gap-8 justify-start items-center relative overflow-hidden">
          <div
            className="eye absolute right-0 h-full w-[40px] rounded-lg text-(--text-primary) flex items-center justify-center cursor-pointer font-bold"
            onClick={() => {
              setEye((prev) => !prev);
            }}
          >
            {eye ? (
              <i className="ti ti-eye text-[25px]"></i>
            ) : (
              <i className="ti ti-eye-off text-[25px]"></i>
            )}
          </div>
          <div className="w-[100px]">Groq Api Key</div>
          <input
            type={eye ? "password" : "text"}
            className="text-(--text-primary) bg-(--message) border-[1px] border-solid border-(--dark-border) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 transition-all duration-250 ease-in"
            placeholder="Enter your Api Key"
            onChange={(e) => {
              setSetting((prev) => ({ ...prev, api_key: e.target.value }));
            }}
            value={setting.api_key}
          />
        </div>
        {/* <div className="name w-full flex gap-8 justify-start items-start">
          <div className="w-[100px]">Llm Mode</div>
          <div className="flex w-[150px] gap-4 items-center justify-center w-full">
            <div className="mode-selector w-full ml-[13px] pl-[15px] border-solid border-[1px] rounded-lg p-[10px] flex gap-[10px] flex-col border-(--dark-border) bg-(--message)">
              <div
                className="w-full flex gap-[20px] items-center justify-start cursor-pointer"
                onClick={() => {
                  setSetting((prev) => ({ ...prev, llm_mode: "qwen" }));
                }}
              >
                <input
                  type="radio"
                  className="qwen cursor-pointer"
                  name="llm_mode"
                  onChange={() => {}}
                  value={setting.llm_mode}
                  checked={setting.llm_mode === "qwen"}
                />
                <div className="shrink-0">
                  <div className="text-[18px]">Local Qwen</div>
                  <div className="text-[13px]">
                    Runs on the user computer. Supports offline use.
                  </div>
                </div>
              </div>
              <div
                className="w-full flex gap-[20px] items-center justify-start cursor-pointer"
                onClick={() => {
                  setSetting((prev) => ({ ...prev, llm_mode: "groq" }));
                }}
              >
                <input
                  type="radio"
                  className="groq cursor-pointer"
                  name="llm_mode"
                  value="groq"
                  checked={setting.llm_mode === "groq"}
                  onChange={() => {}}
                />
                <div className="shrink-0">
                  <div className="text-[18px]">Groq cloud</div>
                  <div className="text-[13px]">
                    Fast responses. Requires internet and an Api Key
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div> */}
        <button
          className="save self-start bg-[linear-gradient(135deg,#b06bff,#5b8bff)] rounded-lg h-[40] px-[10px] py-[5px] cursor-pointer transition-all active:scale-95 duration-250 ease-in"
          onClick={async () => {
            try {
              let response = await settingConnect(setting);
              if (response.message) {
                setAlert({ msg: response.message, state: true });
                let data = await fetchSetting();
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
