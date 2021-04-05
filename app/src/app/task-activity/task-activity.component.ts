// global
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage, AppConfig } from "../models/config";
import { UtilsService } from "../services/utils.service";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-task-activity",
  templateUrl: "./task-activity.component.html",
  styleUrls: ["./task-activity.component.scss"],
})
export class TaskActivityComponent implements OnInit {
  appConfig: any;
  capitalize: any;
  unableToLoad: any;
  assets: any;

  constructor(
    public session: SessionPage,
    private router: Router,
    private titleService: Title,
    private utilsService: UtilsService
  ) {
    this.appConfig = AppConfig; // for use in HTML
    this.capitalize = this.utilsService.capitalize; // for use in the HTML
  }

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    this.assets = this.appConfig[this.session.appMode]; // get task assets
    if (this.session.appOrder && this.session.appType) {
      switch (this.session.appMode) {
        case "service":
          this.unableToLoad = false; // load the app!
          this.titleService.setTitle("Service");
          break;
        case "cooking":
          this.unableToLoad = false; // load the app!
          this.titleService.setTitle("Cooking");
          break;
        case "practice":
          this.titleService.setTitle("Error");
          break;
        default:
          this.titleService.setTitle("Error");
          break;
      }
    } else {
      this.titleService.setTitle("Error");
    }
  }

  getReviews() {
    // collect reviews
    let allReviews = this.assets.task.reviews;
    let reviews = [];
    if (this.session.appType == "BOTH") {
      reviews = [...allReviews["BTWN"], ...allReviews["WTHN"]];
    } else {
      reviews = allReviews[this.session.appType];
    }
    // randomly sort them
    for (let i = reviews.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [reviews[i], reviews[j]] = [reviews[j], reviews[i]];
    }
    return reviews;
  }

  next() {
    switch (this.session.appMode) {
      case "service":
        this.session.task_service.complete(new Date().getTime());
        this.router.navigateByUrl("/live-service");
        break;
      case "cooking":
        this.session.task_cooking.complete(new Date().getTime());
        this.router.navigateByUrl("/live-cooking");
        break;
    }
  }
}
