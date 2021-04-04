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
  selector: "app-post-survey-activity",
  templateUrl: "./post-survey-activity.component.html",
  styleUrls: ["./post-survey-activity.component.scss"],
})
export class PostSurveyActivityComponent implements OnInit, AfterViewInit {
  appConfig: any;
  postSurveyURL: any;
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
    this.postSurveyURL = this.sanitizer.bypassSecurityTrustResourceUrl(
      AppConfig["postSurveyURL"][this.session.appType]
    );
  }

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    if (this.session.appOrder && this.session.appType && this.session.appMode !== "practice") {
      this.surveyHeight = 0; // don't show survey until loaded
      this.inputValid = false; // keep input valid flag false until correct code is typed
      this.iFrameLoaded = false; // once iFrame is loaded this gets set to true
      this.unableToLoad = false; // load page
      this.titleService.setTitle("Post-Survey");
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
    const code = AppConfig["continueCode"]["post-survey-activity"];
    this.inputValid = event.target.value === code ? true : false;
  }

  next() {
    this.session.postsurvey.complete(new Date().getTime());
    this.router.navigateByUrl(`/thanks`);
  }
}
