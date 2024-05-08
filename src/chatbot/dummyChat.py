import markdown

class DummyChat:

    """
    Dummy chat that can be used to troubleshoot the website without an OpenAI API key.
    Needs FRONTEND_ONLY environment variable to be set to a truthy value.
    """

    def __init__(self, *args, **kwargs):
        self.id = 'dummy'
    
    @staticmethod
    def get_streaming_response(*args, **kwargs):

        yield f'data: {markdown.markdown("this is an example response")}\n\n'
        yield 'data: <!END>\n\n'
