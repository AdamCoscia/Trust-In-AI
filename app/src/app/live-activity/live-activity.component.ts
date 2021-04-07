// global
import { Component, OnInit, AfterViewInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
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
  loadingRecommendation: any;
  hideRecommendation: any;
  taskComplete: any;

  constructor(
    public session: SessionPage,
    private titleService: Title,
    private chatService: ChatService,
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
    this.loadingRecommendation = false; // shows loading symbol while fetching recommendation
    this.hideRecommendation = true; // keep recommendation hidden until user asks for it
    this.taskComplete = false; // when finished, set this to true
    if (this.session.appOrder && this.session.appType) {
      this.userConfig[this.session.appMode].appType = this.session.appType; // set appType in user config
      switch (this.session.appMode) {
        case "practice":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Practice"); // set the page title
          this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
          break;
        case "hiring":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Hiring"); // set the page title
          this.chatService.connectToSocket(this); // Connect to Server to Send/Receive Messages over WebSocket
          break;
        case "movies":
          this.unableToLoad = false; // load the page!
          this.titleService.setTitle("Movies"); // set the page title
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
    // get assets from appConfig
    app.assets = app.appConfig[app.session.appMode]; // get task assets
    // subscribe to interaction responses from the server
    app.chatService.getInteractionResponse().subscribe((obj) => {
      if (!app.socketConnected) app.socketConnected = true; // load the page!
    });
    // send init message to initialize PID in server logs and load the page
    let message = app.utilsService.initializeNewMessage(app);
    message.interactionType = InteractionTypes.INITIALIZE_APP;
    app.chatService.sendInteractionResponse(message);
  }

  /**
   * Get card filenames and filepaths to populate cards on page.
   * @returns List of card objects
   */
  getCards() {
    return this.assets.scenarios[this.currentScenario].choices.map((cn: any) => ({
      id: cn,
      filepath: `${this.assets.dir}/cards/${cn}.png`,
    }));
  }

  /**
   * Gets formatted string for card element.
   * @param id Card id
   * @returns String containing id for card element.
   */
  getCardId(id: any) {
    return `card${id}`;
  }

  // =========================== INTERACTION METHODS =========================

  /**
   * Updates user config with currently selected id.
   * @param event Event object
   * @param id Card id
   */
  onSelectCard(event: any, id: any): void {
    if (!this.taskComplete) {
      let app = this;
      // set selected ID in user config
      app.userConfig.selectedId = id;
      // send card clicked message
      let message = app.utilsService.initializeNewMessage(app);
      message.interactionType = InteractionTypes.CARD_CLICKED;
      message.currentScenario = app.currentScenario;
      message.selectedId = app.userConfig.selectedId;
      message.recommendationShown = !app.hideRecommendation;
      app.chatService.sendInteractionResponse(message);
    }
  }

  /**
   * Load recommendation element.
   */
  getRecommendation(): void {
    let app = this;
    // show loading icon
    app.loadingRecommendation = true;
    // show recommendation after 3-5 seconds, randomly
    setTimeout(function () {
      app.loadingRecommendation = false; // hide loading icon
      app.hideRecommendation = false; // show recommendation
      // send recommendation shown interaction message
      let message = app.utilsService.initializeNewMessage(app);
      message.interactionType = InteractionTypes.GET_RECOMMENDATION;
      message.currentScenario = app.currentScenario;
      message.selectedId = app.userConfig.selectedId;
      message.recommendationShown = !app.hideRecommendation;
      app.chatService.sendInteractionResponse(message);
    }, Math.floor(Math.random() * (3.8 - 1.3) + 1.3 * 1000));
  }

  /**
   * Saves selection to user config and prepares next scenario.
   */
  saveSelection(): void {
    let app = this;
    const scenarios = app.assets.scenarios;
    // save a test selections log
    app.userConfig[app.session.appMode].selections.push({
      selectedId: app.userConfig.selectedId,
      botChoice: scenarios[app.currentScenario].choices[scenarios[app.currentScenario].answer],
      recommendationShown: !app.hideRecommendation,
      savedAt: app.utilsService.getCurrentTime(),
    });
    // send selection saved interaction message
    let message = app.utilsService.initializeNewMessage(app);
    message.interactionType = InteractionTypes.SAVE_SELECTION;
    message.currentScenario = app.currentScenario;
    message.selectedId = app.userConfig.selectedId;
    message.recommendationShown = !app.hideRecommendation;
    app.chatService.sendInteractionResponse(message);
    // reset current selection
    app.userConfig.selectedId = "";
    // check for next scenario
    if (app.currentScenario == scenarios.length - 1) {
      app.taskComplete = true; // last scenario reached => enable Finish button
    } else {
      app.hideRecommendation = true; // hide recommendation again
      app.currentScenario++; // increment scenario
    }
  }

  // ============================== PAGE METHODS =============================

  /**
   * Moves the application to the next page.
   */
  next() {
    let app = this;
    // send app closed message
    let message = app.utilsService.initializeNewMessage(app);
    message.interactionType = InteractionTypes.CLOSE_APP;
    app.chatService.sendInteractionResponse(message);
    // save selection logs
    app.chatService.sendMessageToSaveSelectionLog(app.userConfig[app.session.appMode], app.session.participantId);
    // disconnect from socket
    app.chatService.removeAllListenersAndDisconnectFromSocket();
    // Record page complete timestamp
    switch (app.session.appMode) {
      case "practice":
        app.session.live_practice.complete(new Date().getTime());
        break;
      case "hiring":
        app.session.live_hiring.complete(new Date().getTime());
        break;
      case "movies":
        app.session.live_movies.complete(new Date().getTime());
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
