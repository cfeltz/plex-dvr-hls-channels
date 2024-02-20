from fastapi import FastAPI, HTTPException


class ReRouter(FastAPI):

    def __init__(self):
        super().__init__()
        self.service = RequestService()
        self._config = ReRouterConfig(config)


        self.channels = {}
        self._previous_channel_number = None

    @property
    def previous_channel_number(self):
        return self._previous_channel_number

    @previous_channel_number.setter
    def previous_channel_number(self, value):
        if not isinstance(value, int):
            raise Exception("Attempting to set previous channel number to non-int type.")
        self._previous_channel_number = value



app = ReRouter()

@app.get("/reroute/{channel_number}")
def reroute(channel_number):
    # if the previous channel number does not equal the current channel number, we have to do some special shit
    if app.previous_channel_number != channel_number:
        app.service.go_to_url()
        # write the shit to click the player here
        reroute_url = get_shortest_network_request(app.channels[channel_number].regex)
    else:
        reroute_url = get_shortest_network_request(app.channels[channel_number].regex,
                                                               wait_for_network_logs=2)

    app.previous_channel_number = channel_number

    raise HTTPException(status_code=307, detail="Rerouting...", headers={"Location": reroute_url})
