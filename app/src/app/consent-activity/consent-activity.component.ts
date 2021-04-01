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
          this.global.appOrder = ["practice", "service", "cooking"];
          break;
        case "iq0":
          this.global.appOrder = ["practice", "cooking", "service"];
          break;
      }
      // Check for and set appType
      if (this.route.snapshot.queryParams.hasOwnProperty("p2")) {
        switch (this.route.snapshot.queryParams["p2"]) {
          case "t24":
            this.global.appType = "CTRL";
            break;
          case "ozz":
            this.global.appType = "WTHN";
            break;
          case "8gv":
            this.global.appType = "BTWN";
            break;
          case "n5a":
            this.global.appType = "BOTH";
            break;
        }
      }
    }
    if (this.global.appOrder && this.global.appType) {
      this.badURL = false;
      this.titleService.setTitle("Consent");
    } else {
      this.titleService.setTitle("Error");
    }
  }

  usingMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
  }

  next() {
    this.global.consent.complete(new Date().getTime());
    this.router.navigateByUrl("/overview");
  }
}
