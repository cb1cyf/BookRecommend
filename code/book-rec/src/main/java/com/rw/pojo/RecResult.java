package com.rw.pojo;

public class RecResult {
    private Integer userId;
    private Integer bookId;
    private Float rating;

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Integer getBookId() {
        return bookId;
    }

    public void setBookId(Integer bookId) {
        this.bookId = bookId;
    }

    public Float getRating() {
        return rating;
    }

    public void setRating(Float rating) {
        this.rating = rating;
    }

    @Override
    public String toString() {
        return "RecResult{" +
                "userId=" + userId +
                ", bookId=" + bookId +
                ", rating=" + rating +
                '}';
    }
}
