import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreSurveyActivityComponent } from './pre-survey-activity.component';

describe('PreSurveyActivityComponent', () => {
  let component: PreSurveyActivityComponent;
  let fixture: ComponentFixture<PreSurveyActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PreSurveyActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PreSurveyActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
