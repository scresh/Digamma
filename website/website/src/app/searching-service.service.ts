import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable()
export class SearchingServiceService {

  constructor() { }

  aim: {
    what: string,
    whichPage: number,
    howMuchPerPage: number
  };

  search() {

  }

}
