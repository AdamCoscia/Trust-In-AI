// global
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
import { Subscription } from "rxjs";
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
  selector: "app-consent-activity",
  templateUrl: "./consent-activity.component.html",
  styleUrls: ["./consent-activity.component.scss"],
  providers: [ChatService],
})
export class ConsentActivityComponent implements OnInit {
  private subscription: Subscription = new Subscription();

  studyCompleted: any;
  socketConnected: any;
  acceptedConsent: any;

  constructor(
    public session: SessionPage,
    private router: Router,
    private titleService: Title,
    private chatService: ChatService
  ) {}

  ngOnInit(): void {
    this.studyCompleted = true; // whether to load the entire study or not
    this.acceptedConsent = false; // until user clicks 'I Accept' Next button is disabled
    if (!this.studyCompleted) {
      this.titleService.setTitle("Consent"); // set the page title
      this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
    } else {
      this.titleService.setTitle("Thank You!"); // set the page title
    }
  }

  /**
   * Called by chatService when connection is established.
   */
  socketOnConnect(): void {
    let app = this;
    // subscribe to listen for new app state coming from server
    app.subscription.add(
      app.chatService.registerEventHandler(EventTypes.NEW_APP_STATE_RESPONSE).subscribe((obj: any) => {
        if (obj && obj.hasOwnProperty("appType") && obj.hasOwnProperty("appOrder")) {
          app.session.appType = obj.appType;
          app.session.appOrder = obj.appOrder;
          app.socketConnected = true; // load the page!
        }
      })
    );
    // send message to request app state from server
    app.chatService.sendMessage(EventTypes.GET_NEW_APP_STATE, { participantId: app.session.participantId });
  }

  usingMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
  }

  next() {
    // unsubscribe from any event listener streams registered
    this.subscription.unsubscribe();
    // disconnect from the socket
    this.chatService.disconnectFromSocket();
    // record completion time for this activity
    this.session.consent.complete(new Date().getTime());
    // move on to the next page
    this.router.navigateByUrl("/overview");
  }
}
