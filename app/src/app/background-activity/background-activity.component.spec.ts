import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BackgroundActivityComponent } from './background-activity.component';

describe('BackgroundActivityComponent', () => {
  let component: BackgroundActivityComponent;
  let fixture: ComponentFixture<BackgroundActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BackgroundActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BackgroundActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
