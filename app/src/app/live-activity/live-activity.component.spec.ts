import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveActivityComponent } from './live-activity.component';

describe('LiveActivityComponent', () => {
  let component: LiveActivityComponent;
  let fixture: ComponentFixture<LiveActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LiveActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
