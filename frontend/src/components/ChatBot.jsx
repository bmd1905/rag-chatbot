// import avatar from "../assets/avatar.jpg";
import robot_img from "../assets/rem.png";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { TypeAnimation } from "react-type-animation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-svg-icons";
function ChatBot(props) {
  const messagesEndRef = useRef(null);
  const [timeOfRequest, SetTimeOfRequest] = useState(0);
  let [promptInput, SetPromptInput] = useState("");
  let [sourceData, SetSourceData] = useState("nttu");
  let [chatHistory, SetChatHistory] = useState([]);

  const commonQuestions = [
    "Tôi muốn mua quà tặng sinh nhật cho vợ, shop có gợi ý gì không?",
    "Shop còn váy đen không?",
    "Tư vấn cho tôi vài mẫu áo sơ mi phù hợp để đi làm?",
    "Shop có thể tư vấn giúp tôi cách bảo quản áo len để không bị giãn hay xù lông không?",
    "Tôi muốn mua giày cho chồng, làm sao để chọn size chính xác?",
    "Shop có bán phụ kiện như túi xách hoặc ví không?",
    "Có mẫu váy nào phù hợp cho tiệc tối không?",
    "Shop có thể gợi ý quần áo phù hợp cho người dáng gầy không?",
    "Tôi chuẩn bị đi du lịch châu Âu vào cuối năm, shop có thể gợi ý một set đồ ấm áp không?",
    "Shop có bán quần legging không? Giá rẻ nhất là bao nhiêu?",
    "Tôi đang tìm một chiếc váy dạ hội cho buổi tiệc sang trọng, yêu cầu là màu xanh dương, dáng ôm, nhưng không hở quá nhiều. Tôi cao 1m65, nặng 55kg, vòng eo 65cm. Gợi ý cho tôi vài mẫu phù hợp.",
    "Tôi muốn biết giày này có màu khác ngoài màu đen không?",
    "Shop có thể gợi ý trang phục phù hợp cho tiệc cưới ban ngày không? Tôi muốn mặc màu pastel.",
];


  let [isLoading, SetIsLoad] = useState(false);
  let [isGen, SetIsGen] = useState(false);
  const [dataChat, SetDataChat] = useState([
    [
      "start",
      [
        "Xin chào! Tôi có thể giúp gì cho bạn về các sản phẩm của shop BAN?",
        null,
      ],
    ],
  ]);
  useEffect(() => {
    ScrollToEndChat();
  }, [isLoading]);
  useEffect(() => {
    const interval = setInterval(() => {
      SetTimeOfRequest((timeOfRequest) => timeOfRequest + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  function ScrollToEndChat() {
    messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  }
  const onChangeHandler = (event) => {
    SetPromptInput(event.target.value);
  };

  async function SendMessageChat() {
    if (promptInput.trim() === "" || isLoading) {
      return; // Prevent sending empty messages or multiple requests while loading
    }

    try {
      // Reset states
      SetIsGen(true); // Indicate generation is in progress
      SetPromptInput(""); // Clear input field
      SetIsLoad(true); // Show loading spinner or indicator

      // Add user message to chat
      const userMessage = [promptInput, sourceData];
      SetDataChat((prev) => [...prev, ["end", userMessage]]);
      SetChatHistory((prev) => [promptInput, ...prev]);

      // Make API request
      const encodedQuery = encodeURIComponent(promptInput);
      const response = await fetch(`http://127.0.0.1:8000/rag/?q=${encodedQuery}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420",
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();

      // Add bot response to chat
      const botMessage = [result.result || "Không có câu trả lời", null, sourceData];
      SetDataChat((prev) => [...prev, ["start", botMessage]]);
    } catch (error) {
      console.error("Error:", error);

      // Show error message in chat
      const errorMessage = ["Lỗi, không thể kết nối với server", null];
      SetDataChat((prev) => [...prev, ["start", errorMessage]]);
    } finally {
      // Reset loading states
      SetIsLoad(false);
      SetIsGen(false);
    }
  }


  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      SendMessageChat();
    }
  };
  let [reference, SetReference] = useState({
    title: "",
    source: "",
    url: "",
    text: ``,
  });
  const handleReferenceClick = (sources, sourceType) => {
    SetReference({
      title:
        sourceType == "wiki"
          ? sources.metadata.title
          : sources.metadata.page==undefined? "Sổ tay sinh viên 2023" : "Trang " + sources.metadata.page + " (sổ tay SV)",
      source: sourceType == "wiki" ? "Wikipedia" : "Đại học Nguyễn Tất Thành",
      url:
        sourceType == "wiki"
          ? sources.metadata.source
          : "https://ctsv.ntt.edu.vn/sinh-vien-can-biet/",
      text:
        sourceType == "wiki" ? sources.metadata.summary : sources.page_content,
    });
  };
  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-100 h-[85vh] ">
      <div className="hidden lg:block  drawer-side absolute w-64 h-[20vh] left-3 mt-2 drop-shadow-md">
        <div className="menu p-4 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3  overflow-auto scroll-y-auto max-h-[80vh]">
          {/* Sidebar content here */}
          <ul className="menu text-sm">
            <h2 className="font-bold mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)] ">
              Lịch sử trò chuyện
            </h2>
            {chatHistory.length == 0 ? (
              <p className="text-sm text-gray-500">
                Hiện chưa có cuộc hội thoại nào
              </p>
            ) : (
              ""
            )}
            {chatHistory.map((mess, i) => (
              <li key={i}>
                <p>
                  <FontAwesomeIcon icon={faMessage} />
                  {mess.length < 20 ? mess : mess.slice(0, 20) + "..."}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="hidden lg:block  drawer-side absolute w-64 h-[20vh] mt-2 right-3 drop-shadow-md">
        <div className="menu p-4 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3">
          {/* Sidebar content here */}
          <h2 className="font-bold text-sm mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)] ">
            Nguồn tham khảo
          </h2>
          <ul className="menu">
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium">
                 Sendo
                </span>
                <input
                  type="radio"
                  name="radio-10"
                  value={"sendo"}
                  checked={sourceData === "sendo"}
                  onChange={(e) => {
                    SetSourceData(e.target.value);
                  }}
                  className="radio checked:bg-blue-500"
                />
              </label>
            </li>
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium">
                 Tiki
                </span>
                <input
                  value={"tiki"}
                  type="radio"
                  checked={sourceData === "tiki"}
                  onChange={(e) => {
                    SetSourceData(e.target.value);
                  }}
                  name="radio-10"
                  className="radio checked:bg-blue-500"
                />
              </label>
            </li>
          </ul>
        </div>
        <div
          className="menu p-4 w-full min-h-full bg-gray-50 text-base-content
        rounded-2xl mt-3  overflow-auto scroll-y-auto max-h-[43vh]
        scrollbar-thin scrollbar-thumb-gray-300
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full
        "
        >
          {/* Sidebar content here */}
          <ul className="menu text-sm">
            <h2 className="font-bold mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)] ">
              Những câu hỏi phổ biến
            </h2>

            {commonQuestions.map((mess, i) => (
              <li key={i} onClick={() => SetPromptInput(mess)}>
                <p className="max-w-64">
                  <FontAwesomeIcon icon={faMessage} />
                  {mess}
                  {/* {mess.length < 20 ? mess : mess.slice(0, 20) + "..."} */}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className={"flex justify-center h-[80vh]"}>
        {/* Put this part before </body> tag */}
        <input type="checkbox" id="my_modal_6" className="modal-toggle" />
        <div className="modal">
          <div className="modal-box">
            <h3 className="font-bold text-lg">{reference.title}</h3>{" "}
            <p className="font-normal text-sm">Nguồn: {reference.source}</p>
            <p className="py-4 text-sm">
              {reference.text.slice(0, 700) + "..."}
            </p>
            <p className="link link-primary truncate">
              <a href={reference.url} target="_blank">
                {reference.url}
              </a>
            </p>
            <div className="modal-action">
              <label htmlFor="my_modal_6" className="btn btn-error">
                ĐÓNG
              </label>
            </div>
          </div>
        </div>

        <div
          id="chat-area"
          className="
          mt-5 text-sm
          scrollbar-thin scrollbar-thumb-gray-300 bg-white
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full
          rounded-3xl border-2 md:w-[50%] md:p-3 p-1  w-full overflow-auto scroll-y-auto h-[80%] "
        >
          {dataChat.map((dataMessages, i) =>
            dataMessages[0] === "start" ? (
              <div className="chat chat-start drop-shadow-md" key={i}>
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full border-2 border-blue-500">
                    <img className="scale-150" src={robot_img} />
                  </div>
                </div>
                <div className="chat-bubble chat-bubble-info colo break-words ">
                  <TypeAnimation
                    style={{ whiteSpace: 'pre-line' }}
                    sequence={[
                      // () => ScrollToEndChat(),
                      dataMessages[1][0]

                      ,
                      () => SetIsGen(false),
                      // SetIsLoad(false),
                      // .replace("\n\n", "")
                      // .split("\n")
                      // .map((item, key) => {
                      //   return (
                      //     <>
                      //       {item.replace(/ /g, "\u00A0")}
                      //       <br />
                      //     </>
                      //   );
                      // })
                    ]}
                    cursor={false}
                    // wrapper="span"
                    speed={100}
                  />
                  {dataMessages[1][1] === null ||
                  dataMessages[1][1].length == 0 ? (
                    ""
                  ) : (
                    <>
                      <div className="divider m-0"></div>
                      <p className="font-semibold text-xs">
                        Tham khảo:{" "}
                        {dataMessages[1][1].map((source, j) => (
                          <label
                            htmlFor="my_modal_6"
                            className="kbd kbd-xs mr-1 hover:bg-sky-300 cursor-pointer"
                            onClick={() =>
                              handleReferenceClick(source, dataMessages[1][2])
                            }
                            key={j}
                          >
                            {dataMessages[1][2] == "wiki"
                              ? source.metadata.title
                              : source.metadata.page==undefined? "Sổ tay sinh viên 2023" : "Trang " +
                                source.metadata.page +
                                " (sổ tay SV)"}
                          </label>
                        ))}
                      </p>
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="chat chat-end">
                {/* bg-gradient-to-r from-cyan-500 to-blue-500 */}
                <div className="chat-bubble shadow-xl chat-bubble-primary bg-gradient-to-r from-purple-500 to-blue-500 text-white">
                  {dataMessages[1][0]}
                  <>
                    <div className="divider m-0"></div>
                    <p className="font-light text-xs text-cyan-50">
                      Tham khảo:{"Sendo"}
                    </p>
                  </>
                </div>
              </div>
            )
          )}
          {isLoading ? (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-10 rounded-full border-2 border-blue-500">
                  <img src={robot_img} />
                </div>
              </div>
              <div className="chat-bubble chat-bubble-info">
                <ScaleLoader
                  color="#000000"
                  loading={true}
                  height={10}
                  width={10}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
                <p className="text-xs font-medium">{timeOfRequest + "/60s"}</p>
              </div>
            </div>
          ) : (
            ""
          )}
          <div ref={messagesEndRef} />
          <div className="absolute bottom-[0.2rem] md:w-[50%] grid ">
            <input
              type="text"
              placeholder="Nhập câu hỏi tại đây..."
              className="mr-1 shadow-xl border-2 focus:outline-none px-2 rounded-2xl input-primary col-start-1 md:col-end-12 col-end-11 "
              onChange={onChangeHandler}
              onKeyDown={handleKeyDown}
              disabled={isGen}
              value={promptInput}
            />

            <button
              disabled={isGen}
              onClick={() => SendMessageChat()}
              className={
                " drop-shadow-md md:col-start-12 rounded-2xl col-start-11 col-end-12 md:col-end-13 btn btn-active btn-primary btn-square bg-gradient-to-tl from-transparent via-blue-600 to-indigo-500"
              }
            >
              <svg
                stroke="currentColor"
                fill="none"
                strokeWidth="2"
                viewBox="0 0 24 24"
                color="white"
                height="15px"
                width="15px"
                xmlns="http://www.w3.org/2000/svg"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
            <p className=" text-xs col-start-1 col-end-12 text-justify p-1">
              <b>Lưu ý: </b>Mô hình có thể đưa ra câu trả lời không chính xác ở
              một số trường hợp, vì vậy hãy luôn kiểm chứng thông tin bạn nhé!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
export default ChatBot;
