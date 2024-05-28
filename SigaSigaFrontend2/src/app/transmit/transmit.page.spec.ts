import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TransmitPage } from './transmit.page';

describe('TransmitPage', () => {
  let component: TransmitPage;
  let fixture: ComponentFixture<TransmitPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(TransmitPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
