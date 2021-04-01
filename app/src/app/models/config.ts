// libraries
import { Injectable } from "@angular/core";
// local
import { UtilsService } from "../services/utils.service";

var UtilsServiceObj = new UtilsService();
var participantId = UtilsServiceObj.generateRandomUniqueString(12);

class PageRecord {
  completed: any;
  timestamp: any;

  constructor() {
    this.completed = false;
    this.timestamp = null;
  }

  complete(timestamp: any) {
    this.completed = true;
    this.timestamp = timestamp;
  }

  save() {
    return { completed: this.completed, timestamp: this.timestamp };
  }
}

@Injectable()
export class SessionPage {
  participantId: any;
  appOrder: any;
  appType: any;
  appMode: any;
  consent: any;
  overview: any;
  background: any;
  live_practice: any;
  presurvey: any;
  task_service: any;
  live_service: any;
  task_cooking: any;
  live_cooking: any;
  postsurvey: any;
  thanks: any;

  constructor() {
    // ids
    this.participantId = participantId; // 12 character long unique identifier
    // conditions
    this.appOrder = []; // Order of Tasks, e.g., {practice, service, cooking}
    this.appType = ""; // Condition {CTRL, WTHN, BTWN, BOTH}
    // states
    this.appMode = ""; // Current Task
    // pages
    this.consent = new PageRecord();
    this.overview = new PageRecord();
    this.background = new PageRecord();
    this.presurvey = new PageRecord();
    this.task_service = new PageRecord();
    this.live_service = new PageRecord();
    this.task_cooking = new PageRecord();
    this.live_cooking = new PageRecord();
    this.postsurvey = new PageRecord();
    this.thanks = new PageRecord();
  }
}

export const DeploymentConfig = Object.freeze({
  SERVER_URL: "https://cs6795-group-project-server.herokuapp.com/",
});

/**
 * SUPPORTED INTERACTION TYPES
 */
export const enum InteractionTypes {}

/**
 * APPLICATION-SPECIFIC SETTINGS
 */
export const AppConfig: any = {
  /**
   * Security passcodes to prevent the user from spamming the Next button.
   */
  continueCode: {
    "background-activity": "qp5mz",
    "pre-survey-activity": "8sb34",
    "post-survey-activity": "l3h0a",
  },
  /**
   * URLs for embedded Qualtrics surveys.
   */
  backgroundSurveyURL: "", // TODO
  preSurveyURL: "", // TODO
  postSurveyURL: {
    CTRL: "", // TODO
    WTHN: "", // TODO
    BTWN: "", // TODO
    BOTH: "", // TODO
  },
};

/**
 * USER-SPECIFIC SETTINGS
 */
export var UserConfig: any = {
  // TODO
};
