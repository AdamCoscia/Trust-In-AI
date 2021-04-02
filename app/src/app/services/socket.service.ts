// libraries
import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { map } from "rxjs/operators";

@Injectable()
export class ChatService {
  page: any;

  constructor(private socket: Socket) {
    this.socket.on("connect", () => {
      // once connection is established, load the page
      this.page.socketConnected = true;
      this.page.socketOnConnect();
    });
  }

  connectToSocket(app: any) {
    this.page = app; // save reference to page
    this.socket.connect();
  }

  removeAllListenersAndDisconnectFromSocket() {
    this.socket.removeAllListeners();
    this.socket.disconnect();
  }

  sendInteractionResponse(payload: any) {
    this.socket.emit("on_interaction", payload);
  }

  getInteractionResponse() {
    return this.socket.fromEvent("interaction_response").pipe(map((data) => data));
  }

  sendMessageToSaveSessionLog(data: any, pid: any) {
    let payload = {
      log: data,
      pid: pid,
    };
    this.socket.emit("save_session_log", payload);
  }

  sendMessageToSaveSelectionLog(data: any, pid: any) {
    let payload = {
      log: data,
      pid: pid,
    };
    this.socket.emit("save_selection_log", payload);
  }
}
