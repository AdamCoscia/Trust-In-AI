// libraries
import { Component, OnInit } from "@angular/core";
import { Router, ActivatedRoute } from "@angular/router";
import { Title } from "@angular/platform-browser";
// local
import { SessionPage } from "../models/config";

window.addEventListener("beforeunload", function (e) {
  // Cancel the event
  e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  // Chrome requires returnValue to be set
  e.returnValue = "";
});

@Component({
  selector: "app-consent-activity",
  templateUrl: "./consent-activity.component.html",
  styleUrls: ["./consent-activity.component.scss"],
})
export class ConsentActivityComponent implements OnInit {
  acceptedConsent: any;
  badURL: any;

  constructor(
    public global: SessionPage,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {
    this.acceptedConsent = false; // until user clicks 'I Accept' Next button is disabled
    this.badURL = true; // assume poorly formatted URL until all parameters can be verified
  }

  ngOnInit(): void {
    // Check for and set appOrder
    if (this.route.snapshot.queryParams.hasOwnProperty("p1")) {
      switch (this.route.snapshot.queryParams["p1"]) {
        case "95u":
          this.global.appOrder = ["service", "cooking"];
          break;
        case "iq0":
          this.global.appOrder = ["cooking", "service"];
          break;
      }
      // Check for and set appType
      if (this.route.snapshot.queryParams.hasOwnProperty("p2")) {
        switch (this.route.snapshot.queryParams["p2"]) {
          case "t24":
            this.global.appType = "c1";
            break;
          case "ozz":
            this.global.appType = "c2";
            break;
          case "8gv":
            this.global.appType = "c3";
            break;
          case "n5a":
            this.global.appType = "c4";
            break;
        }
      }
    }
    if (this.global.appOrder && this.global.appType) {
      // appOrder and appType were set above => show consent doc!
      this.titleService.setTitle("Consent");
      this.badURL = false;
    } else {
      this.titleService.setTitle("Error");
    }
  }

  usingMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
  }

  next(path: any) {
    this.global.consent.complete(new Date().toLocaleString());
    this.router.navigateByUrl(path);
  }
}
