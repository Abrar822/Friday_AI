export default function Alert({msg}) {
	return (
		<>
			<div className="alert-container absolute z-10 h-[50px] w-[100%] flex justify-center items-start top-[30px]">
				<div className="msg absolute max-w-[500px] bg-(--text-primary) text-[black] py-2 px-4 rounded-xl text-center flex justify-center items-center font-bold min-w-[250px]">{msg}</div>
			</div>
		</>
	)
}