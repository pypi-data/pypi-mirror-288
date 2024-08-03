from PIL import Image
import streamlit as st
from importlib.resources import path


# Sidebar extra widget is a callable that is called in the sidebar
# Default value is noop
def tool_selector(
    tools,
    tool_config_parser: callable,
    app_name: str,
    sidebar_extra_widget: callable = lambda: None,
):
    """
    Display and manage the selection interface for choosing among available tools in a Streamlit application.

    Parameters:
        tools (list[BaseToolConfig]): A list of `BaseToolConfig` objects representing different tools.
        tool_config_parser (callable): A function that processes each `BaseToolConfig` object to prepare
                                       it for display and execution. This typically involves parsing the configuration
                                       and binding it to an executable function.
        app_name (str): The name of the Streamlit application, used as a title in the sidebar.
        sidebar_extra_widget (callable, optional): An additional callable widget that can be displayed in the sidebar,
                                                   such as advanced settings. Defaults to a no-operation lambda.

    Description:
        This function is designed to be used within a Streamlit app where it presents users with a selection
        interface for tools.
        It uses session state to manage the currently selected tool. The `tool_config_parser` is called
        with each `BaseToolConfig` object from the `tools` list, allowing dynamic execution logic based on
        individual tool configurations.

    Example Usage:
        >>> def parse_tools_config(tools):
        ...     # Process tools and bind them to executable functions.
        ...     parsed_tools = {}
        ...     for tool in tools:
        ...         if tool.config.type == "chat":
        ...             parsed_tools[tool.config.name] = lambda tool=tool: chat_tool(tool.config.prompt, LLM_CONFIG_ID)
        ...         elif tool.config.type == "writing-assistant":
        ...             parsed_tools[tool.config.name] = lambda tool=tool: multi_tool(tool.config, llm_api_handler)
        ...     return parsed_tools
        ...
        >>> available_tools = [BaseToolConfig(name="Chat Tool", type="chat"), BaseToolConfig(name="Writing Assistant", type="writing-assistant")]
        >>> tool_selector(available_tools, parse_tools_config, "My Streamlit App")
    """

    print(f"tools in tool selector refactored: {tools}")
    if "tool" not in st.session_state:
        st.session_state["tool"] = tools[0].config.name
    tools = tool_config_parser(tools)
    print(f"tools in tool selector refactored after parsing: {tools}")

    def select_tool(tool_name: str):
        st.session_state["tool"] = tool_name

    with st.sidebar:
        with path("playgroundutils.media", "logo.png") as favicon_path:
            favicon = favicon_path.read_bytes()
            st.image(favicon)
        st.markdown(
            f"<h1 style='text-align: center;'>{app_name}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        for tool in tools:
            st.button(
                tool,
                on_click=select_tool,
                args=(tool,),
                use_container_width=True,
            )
        st.markdown("---")
        sidebar_extra_widget()

    if st.session_state["tool"] in tools:
        print(f"calling lambda tools[{st.session_state['tool']}]\n")
        tools[st.session_state["tool"]]()


def init_streamlit_app(title: str = ""):
    """
    Initialize the Streamlit application with standardized configuration.

    Parameters:
        title (str, optional): The title of the Streamlit app. Defaults to an empty string.

    Description:
        This function sets up a Streamlit application's page configuration and custom styling.
        This can only be called as the first Streamlit function. The function configures the page layout,
        sidebar padding, logo positioning, background colors, and font sizes for improved user experience.

    Usage Example:
        >>> init_streamlit_app("My Cool App")
        # Initializes a Streamlit app titled "My Cool App".
    """
    # TODO: favicon_path as parameter
    with path("playgroundutils.media", "Favicon.png") as favicon_path:
        image = Image.open(favicon_path)
    st.set_page_config(
        page_title=title,
        page_icon=image,
        layout="centered",
        initial_sidebar_state="auto",
    )
    st.markdown(
        """
                <style>
                    section[data-testid="stSidebar"] > :nth-child(1) > :nth-child(2) {
                        padding-top: 2.6rem;
                    }
                    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > :nth-child(1) img {
                        padding: 0.5rem;
                    }
                    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > :nth-child(2) {
                        margin-top: 2rem;
                    }
                    .stChatFloatingInputContainer {
                        background: #1a1e33;
                    }
                    .main .block-container {
                        background: transparent;
                    }
                    .main .block-container p,
                    .main .block-container ol,
                    .main .block-container ul,
                    .main .block-container dl,
                    .main .block-container li {
                        font-size: 1.4rem;
                    }
                    .main .block-container code {
                        font-size: 1.2rem;
                    }
                </style>
                """,
        unsafe_allow_html=True,
    )
