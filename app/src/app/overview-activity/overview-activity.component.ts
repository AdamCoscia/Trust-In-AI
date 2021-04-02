// global
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";
import { UtilsService } from "../services/utils.service";

@Component({
  selector: "app-overview-activity",
  templateUrl: "./overview-activity.component.html",
  styleUrls: ["./overview-activity.component.scss"],
})
export class OverviewActivityComponent implements OnInit {
  unableToLoad: any;
  capitalize: any;

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
      this.unableToLoad = false;
      this.titleService.setTitle("Overview");
    } else {
      this.titleService.setTitle("Error");
    }
  }

  next() {
    this.session.overview.complete(new Date().getTime());
    this.router.navigateByUrl("/background");
  }
}
