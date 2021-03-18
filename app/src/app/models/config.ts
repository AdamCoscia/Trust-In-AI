// libraries
import { Injectable } from '@angular/core';
// local
import { UtilsService } from '../services/utils.service';

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
  constructor(private utils: UtilsService) {}
  // ids
  'participantId': string = participantId; // 12 character long unique identifier
  // conditions
  'appOrder': string[] = []; // Order of Tasks
  'appType': string = ''; // Condition {c1, c2, c3, c4}
  // states
  'appMode': string = 'service'; // Task {service, cooking}
  // pages
  'consent' = new PageRecord();
  'overview' = new PageRecord();
  'pre-survey' = new PageRecord();
  'task-service' = new PageRecord();
  'live-service' = new PageRecord();
  'task-cooking' = new PageRecord();
  'live-cooking' = new PageRecord();
  'post-survey' = new PageRecord();
  'thanks' = new PageRecord();
}

export const DeploymentConfig = Object.freeze({
  SERVER_URL: 'http://localhost:3000',
  PRE_SURVEY_FORM_URL: '', // TODO
  POST_SURVEY_FORM_URL: {
    c1: '', // TODO
    c2: '', // TODO
    c3: '', // TODO
    c4: '', // TODO
  },
});

/**
 * SUPPORTED INTERACTION TYPES
 */
export const enum InteractionTypes {}
// TODO

/**
 * USER SPECIFIC SETTINGS
 */
export var UserConfig = {
  // TODO
};

/**
 * TASK SPECIFIC SETTINGS
 */
export const AppConfig = {
  // TODO
};
