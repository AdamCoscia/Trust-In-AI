// libraries
import { Injectable } from "@angular/core";
// local
import { UtilsService } from "../services/utils.service";
import practiceScenarios from "../../assets/practice/scenarios.json";
import serviceTask from "../../assets/service/task.json";
import serviceScenarios from "../../assets/service/scenarios.json";
import cookingTask from "../../assets/cooking/task.json";
import cookingScenarios from "../../assets/cooking/scenarios.json";

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
    this.live_practice = new PageRecord();
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
  // SERVER_URL: "https://cs6795-group-project-server.herokuapp.com/",
  SERVER_URL: "http://localhost:3000",
});

/**
 * SUPPORTED INTERACTION TYPES
 */
export const enum InteractionTypes {
  INITIALIZE_APP = "init_app",
}

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
    "post-survey-activity": "e3h0a",
  },
  /**
   * URLs for embedded Qualtrics surveys.
   */
  backgroundSurveyURL: "https://gatech.co1.qualtrics.com/jfe/form/SV_7OIzFHat7ALsmZo",
  preSurveyURL: "https://gatech.co1.qualtrics.com/jfe/form/SV_6zdbHRJf6D2NKDA",
  postSurveyURL: {
    CTRL: "https://gatech.co1.qualtrics.com/jfe/form/SV_4MB48PzlEKHIE5w",
    WTHN: "https://gatech.co1.qualtrics.com/jfe/form/SV_4MB48PzlEKHIE5w",
    BTWN: "https://gatech.co1.qualtrics.com/jfe/form/SV_4MB48PzlEKHIE5w",
    BOTH: "https://gatech.co1.qualtrics.com/jfe/form/SV_4MB48PzlEKHIE5w",
  },
  /**
   * PRACTICE MODE
   */
  practice: {
    dir: "assets/practice",
    cards: [1, 2, 3, 4],
    scenarios: practiceScenarios,
  },
  /**
   * SERVICE MODE
   */
  service: {
    dir: "assets/service",
    cards: Array.apply(null, Array(50)).map(function (_, i) {
      return i + 1;
    }),
    task: serviceTask,
    scenarios: serviceScenarios,
  },
  /**
   * COOKING MODE
   */
  cooking: {
    dir: "assets/cooking",
    cards: [1, 2, 3, 4],
    task: cookingTask,
    scenarios: cookingScenarios,
  },
};

/**
 * USER-SPECIFIC SETTINGS
 */
export var UserConfig: any = {
  selectedCandidateId: "",
  /**
   * PRACTICE MODE
   */
  practice: {
    participantId: participantId,
    appMode: "practice",
    appType: "",
    selections: [],
  },
  /**
   * SERVICE MODE
   */
  service: {
    participantId: participantId,
    appMode: "service",
    appType: "",
    selections: [],
  },
  /**
   * COOKING MODE
   */
  cooking: {
    participantId: participantId,
    appMode: "cooking",
    appType: "",
    selections: [],
  },
};
