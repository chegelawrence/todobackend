from flask import jsonify


def return_404():
    return jsonify({
        'msg':'Resource not found'
    }), 404
    