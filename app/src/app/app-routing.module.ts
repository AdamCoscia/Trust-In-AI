import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ConsentActivityComponent } from './consent-activity/consent-activity.component';
import { OverviewActivityComponent } from './overview-activity/overview-activity.component';
import { PreSurveyActivityComponent } from './pre-survey-activity/pre-survey-activity.component';
import { TaskActivityComponent } from './task-activity/task-activity.component';
import { LiveActivityComponent } from './live-activity/live-activity.component';
import { PostSurveyActivityComponent } from './post-survey-activity/post-survey-activity.component';
import { ThanksActivityComponent } from './thanks-activity/thanks-activity.component';

const routes: Routes = [
  // pre-tasks
  { path: '', component: ConsentActivityComponent },
  { path: 'consent', component: ConsentActivityComponent },
  { path: 'overview', component: OverviewActivityComponent },
  { path: 'pre-survey', component: PreSurveyActivityComponent },
  // appMode == service
  { path: 'task-service', component: TaskActivityComponent },
  { path: 'live-service', component: LiveActivityComponent },
  // appMode == cooking
  { path: 'task-cooking', component: TaskActivityComponent },
  { path: 'live-cooking', component: LiveActivityComponent },
  // post-tasks
  { path: 'post-survey', component: PostSurveyActivityComponent },
  { path: 'thanks', component: ThanksActivityComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'enabled' })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
