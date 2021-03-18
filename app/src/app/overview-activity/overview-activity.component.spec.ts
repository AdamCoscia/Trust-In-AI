import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverviewActivityComponent } from './overview-activity.component';

describe('OverviewActivityComponent', () => {
  let component: OverviewActivityComponent;
  let fixture: ComponentFixture<OverviewActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OverviewActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OverviewActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
