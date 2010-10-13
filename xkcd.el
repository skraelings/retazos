;;; xkcd.el --- Download your favorite XKCD episodes from within Emacs

;; Copyright (C) 2010  Reynaldo Baquerizo

;; Author: Reynaldo Baquerizo <reynaldomic@gmail.com>
;; Keywords: comic, xkcd

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:

;;; Code:
(require 'cl)
(require 'xml)
(require 'sgml-mode)

(defconst xkcd-path-to-dir "~/xkcd/"
  "Our directory that contains xkcd comics.")

(defun xkcd-parse-response (buffer)
  "Return a list with the url of the png file, the title and alt.
Argument BUFFER is the output of `url-retrieve-synchronously' command."
  (with-current-buffer buffer
    (url-http-parse-response)
    (search-forward "contentContainer")
    (sgml-skip-tag-backward 1)
    (forward-sexp)
    (let ((start-tag (point))
	  (end-tag (progn (sgml-skip-tag-forward 1)
			  (point))))
      (narrow-to-region start-tag end-tag)
      (beginning-of-buffer)
      (search-forward-regexp "<img src=")
      (if (looking-at "\"http://imgs.xkcd.com/comics")
	  (progn (sgml-skip-tag-backward 1)
		 (setq data (xml-parse-tag))))))
  (kill-buffer buffer)
  data)

(defun xkcd-save-image (buffer title)
  "Save the PNG data found in BUFFER with TITLE in the xkcd
directory as given by the constant xkcd-path-to-dir."
  (with-current-buffer buffer
    (goto-char (1+ url-http-end-of-headers))
    (setq inhibit-read-only t)
    (kill-ring-save (point) (goto-char (point-max)))
    (with-current-buffer (get-buffer-create title)
      (yank)
      (unless (file-directory-p xkcd-path-to-dir)
	(make-directory xkcd-path-to-dir))
      (write-file (concat xkcd-path-to-dir
			  title))
      (kill-buffer))
    (kill-buffer buffer)))

(defun xkcd-retrieve (number)
  "Retrieve an episode of the strip comic XKCD and save it in the XKCD
directory as given by the constant xkcd-path-to-dir.  Return t on
success.  Argument NUMBER is an integer that corresponds to one of the
comics."
  (let* ((buffer (url-retrieve-synchronously
		  (concat "http://xkcd.com/"
			  number)))
	 (attrs (xkcd-parse-response buffer))
	 (src (cdr (assq 'src (car (cdr attrs))))))
    (xkcd-save-image (url-retrieve-synchronously src)
		     (concat number "-"
			     (file-name-nondirectory src)))))

(provide 'xkcd)
;;; xkcd.el ends here
