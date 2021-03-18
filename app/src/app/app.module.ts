import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ConsentActivityComponent } from './consent-activity/consent-activity.component';
import { OverviewActivityComponent } from './overview-activity/overview-activity.component';
import { PreSurveyActivityComponent } from './pre-survey-activity/pre-survey-activity.component';
import { PostSurveyActivityComponent } from './post-survey-activity/post-survey-activity.component';
import { LiveActivityComponent } from './live-activity/live-activity.component';
import { TaskActivityComponent } from './task-activity/task-activity.component';
import { ThanksActivityComponent } from './thanks-activity/thanks-activity.component';

@NgModule({
  declarations: [
    AppComponent,
    ConsentActivityComponent,
    OverviewActivityComponent,
    PreSurveyActivityComponent,
    PostSurveyActivityComponent,
    LiveActivityComponent,
    TaskActivityComponent,
    ThanksActivityComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
