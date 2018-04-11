import { TestBed, inject } from '@angular/core/testing';

import { SearchingServiceService } from './searching-service.service';

describe('SearchingServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SearchingServiceService]
    });
  });

  it('should be created', inject([SearchingServiceService], (service: SearchingServiceService) => {
    expect(service).toBeTruthy();
  }));
});
