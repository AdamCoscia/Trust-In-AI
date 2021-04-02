// global
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
  unableToLoad: any;
  acceptedConsent: any;

  constructor(
    public session: SessionPage,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    this.acceptedConsent = false; // until user clicks 'I Accept' Next button is disabled
    this.unableToLoad = true; // assume poorly formatted URL until all parameters can be verified
    if (this.route.snapshot.queryParams.hasOwnProperty("p1")) {
      switch (this.route.snapshot.queryParams["p1"]) {
        case "95u":
          this.session.appOrder = ["practice", "service", "cooking"];
          break;
        case "iq0":
          this.session.appOrder = ["practice", "cooking", "service"];
          break;
      }
      // Check for and set appType
      if (this.route.snapshot.queryParams.hasOwnProperty("p2")) {
        switch (this.route.snapshot.queryParams["p2"]) {
          case "t24":
            this.session.appType = "CTRL";
            break;
          case "ozz":
            this.session.appType = "WTHN";
            break;
          case "8gv":
            this.session.appType = "BTWN";
            break;
          case "n5a":
            this.session.appType = "BOTH";
            break;
        }
      }
    }
    if (this.session.appOrder && this.session.appType) {
      this.unableToLoad = false;
      this.titleService.setTitle("Consent");
    } else {
      this.titleService.setTitle("Error");
    }
  }

  usingMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
  }

  next() {
    this.session.consent.complete(new Date().getTime());
    this.router.navigateByUrl("/overview");
  }
}
