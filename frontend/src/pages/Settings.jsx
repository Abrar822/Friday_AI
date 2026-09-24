import { settingConnect, fetchSetting } from "../helper/setting_api"

export default function Settings({setting, setSetting, setAlert}) {
  return (
    <>
      <div className="setting-container max-w-[730px] min-w-[500px] w-full bg-(--sidebar-bg) text-(--text-primary) border-solid border-[1px] border-(--dark-border) ml-[90px] mt-[90px] px-[15px] py-[10px] rounded-xl flex flex-col justify-start items-center gap-6">
        <div className="name w-full flex gap-8 justify-start items-center">
          <div className="w-[80px]">Name</div>
          <input type="text" className="text-black bg-(--text-secondary) focus:bg-(--text-primary) py-[4px] px-[10px] rounded-lg h-[35px] flex-1 transition-all duration-250 ease-in" placeholder="Enter your name" onChange={(e) => {
            setSetting({name: e.target.value})
          }} value={setting.name} />
        </div>
        <button className="save self-start bg-[linear-gradient(135deg,#b06bff,#5b8bff)] rounded-lg h-[40] px-[10px] py-[5px] cursor-pointer transition-all active:scale-95 duration-250 ease-in" onClick={async () => {
          try {
            let response = await settingConnect(setting)
            if(response.message) {
              setAlert({msg: response.message, state: true})
              let data = await fetchSetting()
              setSetting({name: data.name})
            }
          } catch(err) {
            setAlert({msg: err.message, state: true})
          }
        }}>Save Changes</button>
      </div>
    </>
  )
}
