// libraries
import { Injectable } from '@angular/core';
// local
import { UtilsService } from '../services/utils.service';

var UtilsServiceObj = new UtilsService();
var participantId = UtilsServiceObj.generateRandomUniqueString(12);

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
  'consent': object = { completed: false, timestamp: 0 };
  'overview': object = { completed: false, timestamp: 0 };
  'pre-survey': object = { completed: false, timestamp: 0 };
  'task-service': object = { completed: false, timestamp: 0 };
  'live-service': object = { completed: false, timestamp: 0 };
  'task-cooking': object = { completed: false, timestamp: 0 };
  'live-cooking': object = { completed: false, timestamp: 0 };
  'post-survey': object = { completed: false, timestamp: 0 };
  'thanks': object = { completed: false, timestamp: 0 };
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
