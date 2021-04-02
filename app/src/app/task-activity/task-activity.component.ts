// global
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";
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
  capitalize: any;
  unableToLoad: any;

  constructor(
    public session: SessionPage,
    private router: Router,
    private titleService: Title,
    private utilsService: UtilsService
  ) {
    this.capitalize = this.utilsService.capitalize; // for use in the HTML
  }

  ngOnInit(): void {
    this.unableToLoad = true; // assume unable to load until all parameters can be verified
    if (this.session.appOrder && this.session.appType) {
      switch (this.session.appMode) {
        case "service":
          this.unableToLoad = false;
          this.titleService.setTitle("Service");
          break;
        case "cooking":
          this.unableToLoad = false;
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
