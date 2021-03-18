import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThanksActivityComponent } from './thanks-activity.component';

describe('ThanksActivityComponent', () => {
  let component: ThanksActivityComponent;
  let fixture: ComponentFixture<ThanksActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThanksActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ThanksActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
