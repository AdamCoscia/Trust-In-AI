// global
import { Component, OnInit, AfterViewInit } from "@angular/core";
import { Router } from "@angular/router";
import { DomSanitizer, Title } from "@angular/platform-browser";
// local
import { Message } from "../models/message";
import { ChatService } from "../services/socket.service";
import { UtilsService } from "../services/utils.service";
import { SessionPage, AppConfig, InteractionTypes, UserConfig } from "../models/config";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-live-activity",
  templateUrl: "./live-activity.component.html",
  styleUrls: ["./live-activity.component.scss"],
  providers: [ChatService],
})
export class LiveActivityComponent implements OnInit, AfterViewInit {
  capitalize: any;
  appConfig: any;
  userConfig: any;
  unableToLoad: any;
  socketConnected: any;
  assets: any;
  currentScenario: any;
  taskComplete: any;

  constructor(
    public session: SessionPage,
    private titleService: Title,
    private chatService: ChatService,
    private message: Message,
    private utilsService: UtilsService,
    private router: Router
  ) {
    this.appConfig = AppConfig; // for use in HTML
    this.userConfig = UserConfig; // for use in HTML
    this.capitalize = this.utilsService.capitalize; // for use in the HTML
  }

  // ========================= INITIALIZATION METHODS ========================

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    this.socketConnected = false; // hide app HTML until socket connnection is established
    this.currentScenario = 0; // scenario number => increment by 1
    this.taskComplete = false; // when finished, set this to true
    this.assets = this.appConfig[this.session.appMode]; // get task assets
    if (this.session.appOrder && this.session.appType) {
      switch (this.session.appMode) {
        case "practice":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Practice"); // set the page title
          this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
          break;
        case "service":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Service"); // set the page title
          this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
          break;
        case "cooking":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Cooking"); // set the page title
          this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
          break;
        default:
          this.titleService.setTitle("Error");
          break;
      }
    } else {
      this.titleService.setTitle("Error");
    }
  }

  ngAfterViewInit(): void {}

  /**
   * Called by chatService when connection is established.
   */
  socketOnConnect(): void {
    let app = this;
    // subscribe to interaction responses from the server
    app.chatService.getInteractionResponse().subscribe((obj) => {});
    // send init message to initialize PID in server logs
    let message = this.utilsService.initializeNewMessage(app);
    message.interactionType = InteractionTypes.INITIALIZE_APP;
    app.chatService.sendInteractionResponse(message);
    // get cards
    let cards = app.getCards();
    console.log(cards);
  }

  // =========================== INTERACTION METHODS =========================

  getCards() {
    return this.assets.scenarios[this.currentScenario].choices.map((cn: any) => ({
      id: cn,
      fp: `${this.assets.dir}/cards/${cn}.png`,
    }));
  }

  getCardId(id: any) {
    return `candidate${id}`;
  }

  onSelectCandidate(event: any, id: any): void {
    this.taskComplete = true;
    const currID = this.userConfig.selectedCandidateId;
    if (currID !== id) this.userConfig.selectedCandidateId = id;
  }

  // ============================== PAGE METHODS =============================

  saveSelections(): void {
    // save a test selections log
    let selections = {
      appMode: this.session.appMode,
      t1: ["p1", this.utilsService.getCurrentTime()],
    };
    this.chatService.sendMessageToSaveSelectionLog(selections, this.session.participantId);
  }

  /**
   * Moves the application to the next page.
   */
  next() {
    let app = this;
    // disconnect from socket
    app.chatService.removeAllListenersAndDisconnectFromSocket();
    // Record page complete timestamp
    switch (app.session.appMode) {
      case "practice":
        app.session.live_practice.complete(new Date().getTime());
        break;
      case "service":
        app.session.live_service.complete(new Date().getTime());
        break;
      case "cooking":
        app.session.live_cooking.complete(new Date().getTime());
        break;
    }
    // Move on to the next page
    let idx = app.session.appOrder.indexOf(app.session.appMode); // get current index of current appMode
    if (idx == 0) {
      // finished practice mode => move on to pre-survey
      app.router.navigateByUrl("/pre-survey");
    } else if (idx < app.session.appOrder.length - 1) {
      // still have tasks to do => to the next task page
      app.session.appMode = app.session.appOrder[idx + 1]; // get next appMode in the list
      app.router.navigateByUrl(`/task-${app.session.appMode}`);
    } else {
      // reached the final task => move on to post-survey
      app.router.navigateByUrl("/post-survey");
    }
  }
}
