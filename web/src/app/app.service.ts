import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class AppService {

    constructor(private http: HttpClient) {
    }

    private parseTime(time: { hour: number, minute: number }) {
        return time && time.hour * 60 + time.minute || 999;
    }

    private page(page) {
        return page ? (page - 1) * 10 : 0;
    }

    public get(filter: { keywords?: string, dinners?: number, difficulty?: number, max_time?: any, last_update?: any }, page = 0) {
        const body = {
            query: {
                bool: {
                    must: {
                        match: {
                            name: filter.keywords || ''
                        }
                    },
                    should: {
                        multi_match: {
                            query: filter.keywords || '',
                            fields: ['ingredients', 'description', 'categories', 'meal_type', 'steps']
                        }
                    },
                    filter: [
                        {
                            range: {
                                last_updated: {
                                    gte: `${filter.last_update.from.year}-${filter.last_update.from.month}-${filter.last_update.from.day}`,
                                    lte: `${filter.last_update.to.year}-${filter.last_update.to.month}-${filter.last_update.to.day}`
                                }
                            }
                        },
                        {range: {dinners: {gte: filter.dinners}}},
                        {range: {difficulty: {lte: filter.difficulty}}},
                        {range: {time: {lte: this.parseTime(filter.max_time)}}}
                    ]
                }
            }
        };
        return this.http.post(
            environment.BASE_URL + `?size=10&from=${this.page(page)}`,
            body,
            {headers: {'Content-Type': 'application/json'}});
    }

}
