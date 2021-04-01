// global
import * as $ from "jquery";
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DomSanitizer, Title } from "@angular/platform-browser";
// local
import { SessionPage, AppConfig } from "../models/config";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-background-activity",
  templateUrl: "./background-activity.component.html",
  styleUrls: ["./background-activity.component.scss"],
})
export class BackgroundActivityComponent implements OnInit {
  appConfig: any;
  badURL: any;
  surveyHeight: any;
  inputValid: any;
  iFrameLoaded: any;
  backgroundSurveyURL: any;

  constructor(
    public global: SessionPage,
    private router: Router,
    private sanitizer: DomSanitizer,
    private titleService: Title
  ) {
    this.badURL = true; // assume poorly formatted URL until all parameters can be verified
    if (this.global.appOrder && this.global.appType) {
      this.badURL = false; // page can load!
      this.titleService.setTitle("Overview");
      this.surveyHeight = 0; // don't show survey until loaded
      this.inputValid = false; // keep input valid flag false until correct code is typed
      this.iFrameLoaded = false; // once iFrame is loaded this gets set to true
      this.appConfig = AppConfig; // for use in HTML
      this.backgroundSurveyURL = this.sanitizer.bypassSecurityTrustResourceUrl(AppConfig["backgroundSurveyURL"]);
    } else {
      this.badURL = true; // don't load page, possible reset
      this.titleService.setTitle("Error");
    }
  }

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    let context = this;
    $("#survey").on("load", () => {
      context.surveyHeight = Math.max(window.innerHeight - 300, 275);
      context.iFrameLoaded = true;
    });
  }

  setSurveyHeight(event: any) {
    if (this.iFrameLoaded) this.surveyHeight = Math.max(window.innerHeight - 300, 275);
  }

  onKey(event: any) {
    const code = AppConfig["continueCode"]["background-activity"];
    this.inputValid = event.target.value === code ? true : false;
  }

  next() {
    this.global.appMode = this.global.appOrder[0]; // set first appMode
    this.global.background.complete(new Date().getTime());
    this.router.navigateByUrl(`/live-${this.global.appMode}`);
  }
}
