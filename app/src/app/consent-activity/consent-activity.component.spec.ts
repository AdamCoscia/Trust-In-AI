import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsentActivityComponent } from './consent-activity.component';

describe('ConsentActivityComponent', () => {
  let component: ConsentActivityComponent;
  let fixture: ComponentFixture<ConsentActivityComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ConsentActivityComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ConsentActivityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
