// libraries
import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";

@Component({
  selector: "app-overview-activity",
  templateUrl: "./overview-activity.component.html",
  styleUrls: ["./overview-activity.component.scss"],
})
export class OverviewActivityComponent implements OnInit {
  badURL: any;

  constructor(public global: SessionPage, private router: Router, private titleService: Title) {
    this.badURL = true; // assume poorly formatted URL until all parameters can be verified
    if (this.global.appOrder && this.global.appType) {
      this.titleService.setTitle("Overview");
      this.badURL = false;
    } else {
      this.titleService.setTitle("Error");
    }
  }

  ngOnInit(): void {}

  next() {
    this.global.overview.complete(new Date().getTime());
    this.router.navigateByUrl("/background");
  }
}
