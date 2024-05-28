import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TransmitirPage } from './transmitir.page';

describe('TransmitirPage', () => {
  let component: TransmitirPage;
  let fixture: ComponentFixture<TransmitirPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(TransmitirPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
