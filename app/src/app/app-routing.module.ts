import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { ConsentActivityComponent } from "./consent-activity/consent-activity.component";
import { OverviewActivityComponent } from "./overview-activity/overview-activity.component";
import { BackgroundActivityComponent } from "./background-activity/background-activity.component";
import { PreSurveyActivityComponent } from "./pre-survey-activity/pre-survey-activity.component";
import { TaskActivityComponent } from "./task-activity/task-activity.component";
import { LiveActivityComponent } from "./live-activity/live-activity.component";
import { PostSurveyActivityComponent } from "./post-survey-activity/post-survey-activity.component";
import { ThanksActivityComponent } from "./thanks-activity/thanks-activity.component";

const routes: Routes = [
  // appMode == ""
  { path: "", component: ConsentActivityComponent },
  { path: "consent", component: ConsentActivityComponent },
  { path: "overview", component: OverviewActivityComponent },
  { path: "background", component: BackgroundActivityComponent },
  // appMode == "practice"
  { path: "live-practice", component: LiveActivityComponent },
  { path: "pre-survey", component: PreSurveyActivityComponent },
  // appMode == "hiring"
  { path: "task-hiring", component: TaskActivityComponent },
  { path: "live-hiring", component: LiveActivityComponent },
  // appMode == "movies"
  { path: "task-movies", component: TaskActivityComponent },
  { path: "live-movies", component: LiveActivityComponent },
  { path: "post-survey", component: PostSurveyActivityComponent },
  { path: "thanks", component: ThanksActivityComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: "enabled" })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
