// libraries
import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { map } from "rxjs/operators";

@Injectable()
export class ChatService {
  page: any;
  activeSubscriptions: any;

  constructor(private socket: Socket) {
    this.activeSubscriptions = [];
    this.socket.on("connect", () => this.page.socketOnConnect());
  }

  connectToSocket(app: any) {
    this.page = app; // save reference to page
    this.socket.connect();
  }

  removeAllListenersAndDisconnectFromSocket() {
    // unsubscribe all event listeners
    for (const evt in this.activeSubscriptions) this.socket.removeAllListeners(evt);
    // clear list of event listeners
    this.activeSubscriptions = [];
    // disconnect from the socket
    this.socket.disconnect();
  }

  sendAppStateRequest(payload: any) {
    this.socket.emit("get_new_app_state", payload);
  }

  getNewAppState() {
    this.activeSubscriptions.push("app_state_response"); // add to active subscriptions
    return this.socket.fromEvent("app_state_response").pipe(map((data) => data));
  }

  sendInteractionResponse(payload: any) {
    this.socket.emit("on_interaction", payload);
  }

  getInteractionResponse() {
    this.activeSubscriptions.push("interaction_response"); // add to active subscriptions
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
