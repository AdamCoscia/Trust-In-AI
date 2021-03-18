// libraries
import { Injectable } from '@angular/core';

@Injectable()
export class UtilsService {
  /**
   * Generates a random alphanumeric string of `length` characters.
   */
  generateRandomUniqueString(length: number) {
    var result = '';
    var characters =
      'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  }

  /**
   * Generates random app type from {c1, c2, c3, c4}
   */
  generateRandomAppType() {
    return Math.random() >= 0.5 ? 'CONTROL' : 'AWARENESS';
  }

  /**
   * Get current time. E.g. usage: timestamp of interaction
   */
  getCurrentTime() {
    return new Date().getTime();
  }
}
