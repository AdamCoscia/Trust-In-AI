// global
import { Component, OnInit } from "@angular/core";
import { Title } from "@angular/platform-browser";
// local
import { ChatService } from "../services/socket.service";
import { SessionPage, EventTypes } from "../models/config";

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
  providers: [ChatService],
})
export class ThanksActivityComponent implements OnInit {
  unableToLoad: any;
  socketConnected: any;

  constructor(private chatService: ChatService, public session: SessionPage, private titleService: Title) {}

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    this.socketConnected = false; // hide app HTML until socket connnection is established
    if (this.session.appOrder && this.session.appType && this.session.appMode !== "practice") {
      this.unableToLoad = false; // page can load!
      this.titleService.setTitle("Thanks");
      this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
    } else {
      this.titleService.setTitle("Error");
    }
  }

  /**
   * Called by chatService when connection is established.
   */
  socketOnConnect(): void {
    // record page complete
    this.session.thanks.complete(new Date().getTime());
    // save message to save the session log to redis
    this.chatService.sendMessage(EventTypes.SAVE_SESSION_LOG, {
      log: this.session,
      pid: this.session["participantId"],
    });
    // disconnect from socket
    this.chatService.disconnectFromSocket();
    // load the page
    this.socketConnected = true;
  }
}
