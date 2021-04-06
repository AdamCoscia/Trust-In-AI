// global
import { Injectable } from "@angular/core";
// local
import { Message } from "../models/message";

@Injectable()
export class UtilsService {
  /**
   * Get current ms since EPOCH.
   */
  getCurrentTime() {
    return new Date().getTime();
  }

  /**
   * Capitalize first letter of alphabetical string.
   * @param word A string of alphabetical chars.
   * @returns The string with the first character uppercase.
   */
  capitalize(word: string) {
    return word.charAt(0).toUpperCase() + word.slice(1);
  }

  /**
   * Generate random alphanumeric string.
   * @param length Number of characters in the generated string.
   * @returns The random string.
   */
  generateRandomUniqueString(length: number) {
    var result = "";
    var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  }

  /**
   * Creates message object to send to server for logging.
   * @param app Application class instance.
   * @returns Message object to populate.
   */
  initializeNewMessage(app: any) {
    let message = new Message();
    (message.participantId = app.session.participantId),
      (message.appMode = app.session.appMode),
      (message.interactionAt = app.utilsService.getCurrentTime()),
      (message.interactionType = ""),
      (message.currentScenario = -1),
      (message.selectedId = -1),
      (message.recommendationShown = false);
    return message;
  }
}
