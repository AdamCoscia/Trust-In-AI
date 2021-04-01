// global
import * as $ from "jquery";
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DomSanitizer, Title } from "@angular/platform-browser";
// local
import { SessionPage, AppConfig, UserConfig } from "../models/config";
import { UtilsService } from "../services/utils.service";

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
})
export class LiveActivityComponent implements OnInit {
  appConfig: any;
  userConfig: any;
  badURL: any;

  constructor(
    public global: SessionPage,
    private router: Router,
    private sanitizer: DomSanitizer,
    private titleService: Title,
    private utils: UtilsService
  ) {
    this.badURL = true; // assume poorly formatted URL until all parameters can be verified
    if (this.global.appOrder && this.global.appType) {
      this.badURL = false; // page can load!
      this.titleService.setTitle("Overview");
      this.appConfig = AppConfig; // for use in HTML
      this.userConfig = UserConfig; // for use in HTML
      this.utils = utils; // for use in HTML
    } else {
      this.badURL = true; // don't load page, possible reset
      this.titleService.setTitle("Error");
    }
  }

  ngOnInit(): void {}

  ngAfterViewInit(): void {}

  next() {
    // Record page complete timestamp
    switch (this.global.appMode) {
      case "practice":
        this.global.live_practice.complete(new Date().getTime());
        break;
      case "service":
        this.global.live_service.complete(new Date().getTime());
        break;
      case "cooking":
        this.global.live_cooking.complete(new Date().getTime());
        break;
    }
    // get next App mode and move on
    let idx = this.global.appOrder.indexOf(this.global.appMode); // get current index of current appMode
    if (idx == -1 || idx >= this.global.appOrder.length) {
      // something went wrong, appMode/appOrder not correct
      this.badURL = true; // show error screen
      this.titleService.setTitle("Error");
    } else if (idx < this.global.appOrder.length - 1) {
      // still have tasks to do => to the next task page
      this.global.appMode = this.global.appOrder[idx + 1]; // get next appMode in the list
      this.router.navigateByUrl(`/task-${this.global.appMode}`);
    } else {
      // reached the final task => move on to post-survey
      this.router.navigateByUrl("/post-survey");
    }
  }
}
