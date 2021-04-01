// libraries
import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { map } from "rxjs/operators";

@Injectable()
export class ChatService {
  constructor(private vizSocket: Socket) {}

  connectToSocket() {
    this.vizSocket.connect();
  }

  sendMessageToSaveSessionLogs(data: any, participantId: any) {
    let payload = {
      logs: data,
      participantId: participantId,
    };
    this.vizSocket.emit("save_session_logs", payload);
  }

  sendMessageToSaveLogs() {
    this.vizSocket.emit("save_interaction_logs");
  }

  sendInteractionResponse(payload: any) {
    this.vizSocket.emit("on_interaction", payload);
  }

  getConnectEventResponse() {
    return this.vizSocket.fromEvent("connect").pipe(map((obj) => obj));
  }

  getDisconnectEventResponse() {
    return this.vizSocket.fromEvent("disconnect").pipe(map((obj) => obj));
  }

  getInteractionResponse() {
    return this.vizSocket.fromEvent("interaction_response").pipe(map((obj) => obj));
  }

  removeAllListenersAndDisconnectFromSocket() {
    this.vizSocket.removeAllListeners();
    this.vizSocket.disconnect();
  }
}
