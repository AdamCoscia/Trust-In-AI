// global
import { Component, OnInit } from "@angular/core";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";
import { ChatService } from "../services/socket.service";
import { UtilsService } from "../services/utils.service";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-thanks-activity",
  templateUrl: "./thanks-activity.component.html",
  styleUrls: ["./thanks-activity.component.scss"],
})
export class ThanksActivityComponent implements OnInit {
  unableToLoad: any;
  socketConnected: any;

  constructor(
    private chatService: ChatService,
    public session: SessionPage,
    private titleService: Title,
    private utilsService: UtilsService
  ) {}

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    this.socketConnected = false; // hide app HTML until socket connnection is established
    if (this.session.appOrder && this.session.appType && this.session.appMode !== "practice") {
      this.unableToLoad = false; // page can load!
      this.titleService.setTitle("Pre-Survey");
      this.subscribeToReceiveMessages(); // Connect to Server to Send/Receive Messages over WebSocket
    } else {
      this.titleService.setTitle("Error");
    }
  }

  init(): void {
    this.session.thanks.complete(new Date().getTime());
    this.chatService.sendMessageToSaveSessionLogs(this.session, this.session["participantId"]);
    this.chatService.removeAllListenersAndDisconnectFromSocket();
  }

  /**
   * Subscribes to server for sending messages.
   */
  subscribeToReceiveMessages() {
    let app = this;
    this.chatService.connectToSocket();
    this.chatService.getConnectEventResponse().subscribe((obj) => {
      console.log("connected to socket");
      app.socketConnected = true; // enable the application
      app.init(); // initialize the app
    });
    this.chatService.getDisconnectEventResponse().subscribe((obj) => {
      console.log("disconnected from socket");
      app.socketConnected = false; // disable the application
    });
  }
}
