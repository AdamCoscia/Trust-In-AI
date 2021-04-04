// global
import { Component, OnInit, AfterViewInit } from "@angular/core";
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
  selector: "app-pre-survey-activity",
  templateUrl: "./pre-survey-activity.component.html",
  styleUrls: ["./pre-survey-activity.component.scss"],
})
export class PreSurveyActivityComponent implements OnInit, AfterViewInit {
  appConfig: any;
  preSurveyURL: any;
  unableToLoad: any;
  surveyHeight: any;
  inputValid: any;
  iFrameLoaded: any;

  constructor(
    public session: SessionPage,
    private router: Router,
    private sanitizer: DomSanitizer,
    private titleService: Title
  ) {
    this.appConfig = AppConfig; // for use in HTML
    this.preSurveyURL = this.sanitizer.bypassSecurityTrustResourceUrl(AppConfig["preSurveyURL"]);
  }

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    if (this.session.appOrder && this.session.appType && this.session.appMode == "practice") {
      this.surveyHeight = 0; // don't show survey until loaded
      this.inputValid = false; // keep input valid flag false until correct code is typed
      this.iFrameLoaded = false; // once iFrame is loaded this gets set to true
      this.unableToLoad = false; // load page!
      this.titleService.setTitle("Pre-Survey");
    } else {
      this.titleService.setTitle("Error");
    }
  }

  ngAfterViewInit(): void {
    let app = this;
    if (!app.unableToLoad) {
      $("#survey").on("load", () => {
        app.surveyHeight = Math.max(window.innerHeight - 300, 275);
        app.iFrameLoaded = true;
      });
    }
  }

  setSurveyHeight(event: any) {
    if (this.iFrameLoaded) this.surveyHeight = Math.max(window.innerHeight - 300, 275);
  }

  onKey(event: any) {
    const code = AppConfig["continueCode"]["pre-survey-activity"];
    this.inputValid = event.target.value === code ? true : false;
  }

  next() {
    this.session.appMode = this.session.appOrder[1]; // go to first task
    this.session.presurvey.complete(new Date().getTime());
    this.router.navigateByUrl(`/task-${this.session.appMode}`);
  }
}
