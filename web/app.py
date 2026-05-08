import sys
import os
from flask import Flask, render_template, request

# Ensure we can import from core_logic regardless of where we run the script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_logic.alignment_engine import compute_global_alignment_matrix, compute_local_alignment_matrix
from core_logic.traceback_engine import reconstruct_alignment_path

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/align", methods=["POST"])
def align():
    try:
        seq1 = request.form.get("seq1", "").strip().upper()
        seq2 = request.form.get("seq2", "").strip().upper()
        match_val = int(request.form.get("match", 1))
        mismatch_val = int(request.form.get("mismatch", -1))
        gap_val = int(request.form.get("gap", -2))
        algorithm = request.form.get("algorithm")

        if not seq1 or not seq2:
            return "Both sequences are required.", 400

        is_local = (algorithm == "local")

        # 1. Generate Matrix
        if is_local:
            matrix, start_i, start_j = compute_local_alignment_matrix(seq1, seq2, match_val, mismatch_val, gap_val)
        else:
            matrix, start_i, start_j = compute_global_alignment_matrix(seq1, seq2, match_val, mismatch_val, gap_val)

        # 2. Reconstruct Path
        align1, align2, score, final_matrix = reconstruct_alignment_path(
            matrix, seq1, seq2, start_i, start_j, is_local
        )

        return render_template(
            "result.html",
            seq1=seq1,
            seq2=seq2,
            align1=align1,
            align2=align2,
            score=score,
            matrix=final_matrix,
            algo_name="Local Alignment (Smith-Waterman)" if is_local else "Global Alignment (Needleman-Wunsch)"
        )

    except ValueError:
        return "Invalid numerical inputs for scoring parameters.", 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)