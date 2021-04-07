// libraries
import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { map } from "rxjs/operators";

@Injectable()
export class ChatService {
  page: any;

  constructor(private socket: Socket) {
    let context = this;
    // call method attached to page that sent the connection request
    context.socket.on("connect", () => context.page.socketOnConnect());
    // NOTE: ensure any Observables created are UNSUBSCRIBED before disconnecting!!
    context.socket.on("disconnect", () => context.socket.removeAllListeners());
  }

  connectToSocket(app: any) {
    this.page = app; // save reference to page
    this.socket.connect(); // connect to socket
  }

  disconnectFromSocket() {
    this.socket.disconnect(); // disconnect from socket
  }

  /**
   * Registers event listener for event and returns `Observable` for event.
   * @param evt Name of event to listen for.
   * @returns `Observable` for event that you can subscribe to.
   */
  registerEventHandler(evt: string) {
    return this.socket.fromEvent(evt).pipe(map((data) => data));
  }

  /**
   * Sends `payload` to server routine specified by `evt`.
   * @param evt Event name specifying server operation to perform.
   * @param payload Data to send to server.
   */
  sendMessage(evt: string, payload: any) {
    this.socket.emit(evt, payload);
  }
}
