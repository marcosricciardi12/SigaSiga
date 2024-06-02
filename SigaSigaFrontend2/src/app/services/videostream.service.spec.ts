import { TestBed } from '@angular/core/testing';

import { VideoStreamService } from './videostream.service';

describe('VideostreamService', () => {
  let service: VideoStreamService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VideoStreamService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
