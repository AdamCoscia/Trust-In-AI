import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostSurveyActivityComponent } from './post-survey-activity.component';

describe('PostSurveyActivityComponent', () => {
  let component: PostSurveyActivityComponent;
  let fixture: ComponentFixture<PostSurveyActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PostSurveyActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PostSurveyActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
