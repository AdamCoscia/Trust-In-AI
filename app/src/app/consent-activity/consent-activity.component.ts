// global
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";
import { ChatService } from "../services/socket.service";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-consent-activity",
  templateUrl: "./consent-activity.component.html",
  styleUrls: ["./consent-activity.component.scss"],
  providers: [ChatService],
})
export class ConsentActivityComponent implements OnInit {
  socketConnected: any;
  acceptedConsent: any;

  constructor(
    public session: SessionPage,
    private router: Router,
    private titleService: Title,
    private chatService: ChatService
  ) {}

  ngOnInit(): void {
    this.acceptedConsent = false; // until user clicks 'I Accept' Next button is disabled
    this.titleService.setTitle("Consent"); // set the page title
    this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
  }

  /**
   * Called by chatService when connection is established.
   */
  socketOnConnect(): void {
    let app = this;
    // subscribe to interaction responses from the server
    app.chatService.getNewAppState().subscribe((obj: any) => {
      if (obj && obj.hasOwnProperty("appType") && obj.hasOwnProperty("appOrder")) {
        app.session.appType = obj.appType;
        app.session.appOrder = obj.appOrder;
        app.socketConnected = true; // load the page!
      } else {
        console.log("Cound not understand incoming server message:");
        console.log(obj);
      }
    });
    // send message to request app state
    app.chatService.sendAppStateRequest({ participantId: app.session.participantId });
  }

  usingMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
  }

  next() {
    this.session.consent.complete(new Date().getTime());
    this.router.navigateByUrl("/overview");
  }
}
