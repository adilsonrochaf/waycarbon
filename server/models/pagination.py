from server import ma


class PaginationSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "page",
            "per_page",
            "total",
            "pages",
            "has_prev",
            "has_next",
            "prev_num",
            "next_num",
        )
