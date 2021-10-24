	.file	"patricia.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.type	bit, @function
bit:
	addi	sp,sp,-32
	mv	t0,s3
	sd	a5,24(sp)
	addi	t1,sp,32
	mv	s1,a0
	sd	a1,-32(t1)
	mv	s0,t0
	mv	ra,s1
	mv	t2,ra
	mv	a4,a4
	addi	a0,s1,817
	mv	s1,s0
	mulhu	a2,a2,t2
	sw	t2,-20(t1)
	andi	s3,s1,-555
	add	t0,s5,s5
	sraw	t6,t6,t5
	mv	sp,t6
	andi	s5,s11,693
	sltu	t2,s5,sp
	mulhsu	s3,s6,s2
	lw	a5,-20(t1)
	mv	sp,a5
	li	a4,-2147483648
	srlw	a5,a4,sp
	sext.w	a5,a5
	sext.w	a5,a5
	mv	a4,a5
	ld	ra,-32(t1)
	sraiw	t2,a1,21
	or	s1,s4,s7
	slt	a0,a1,a3
	sraw	s6,s7,t4
	mv	t1,ra
	ori	a0,a1,-756
	mv	ra,t1
	mulhu	s3,s2,s9
	and	a5,a4,ra
	sra	t6,s2,t5
	and	t6,ra,t1
	sra	t5,s2,t5
	mv	a0,a5
	srlw	s1,t3,t1
	ori	t3,ra,1152
	sllw	s0,s2,s9
	sra	t3,s4,s7
	slti	s5,a1,767
	and	t3,s2,s11
	addi	ra,t1,-395
	sraw	a3,s2,a3
	sltu	a3,t4,ra
	xori	t3,s7,1499
	sub	t1,a7,s2
	mv	s11,s4
	mulw	t5,s8,s2
	mv	a1,sp
	and	s3,s7,s10
	slli	a3,t4,30
	ld	s0,24(a1)
	addi	sp,a1,32
	add	a2,t4,a7
	or	s4,a2,s9
	andi	s6,a6,-2046
	jr	ra
	.size	bit, .-bit
	.align	1
	.type	pat_count, @function
pat_count:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	sw	a5,-44(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-44(s0)
	sext.w	a5,a5
	blt	a5,a4,.L4
	li	a5,0
	j	.L5
.L4:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,24(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	ld	a5,-40(s0)
	ld	a4,32(a5)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	mv	a1,a5
	mv	a0,a4
	call	pat_count
	mv	a5,a0
	mv	a4,a5
	lw	a5,-20(s0)
	addw	a5,a5,a4
	sw	a5,-20(s0)
	lw	a5,-20(s0)
.L5:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	pat_count, .-pat_count
	.align	1
	.type	insertR, @function
insertR:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-24(s0)
	sd	a1,-32(s0)
	mv	a5,a2
	sd	a3,-48(s0)
	sw	a5,-36(s0)
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	ble	a5,a4,.L7
	ld	a5,-24(s0)
	lbu	a4,17(a5)
	ld	a5,-48(s0)
	lbu	a5,17(a5)
	bgtu	a4,a5,.L8
.L7:
	lw	a5,-36(s0)
	andi	a4,a5,255
	ld	a5,-32(s0)
	sb	a4,17(a5)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L9
	ld	a5,-24(s0)
	j	.L10
.L9:
	ld	a5,-32(s0)
.L10:
	ld	a4,-32(s0)
	sd	a5,24(a4)
	ld	a5,-32(s0)
	ld	a4,0(a5)
	lw	a5,-36(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L11
	ld	a5,-32(s0)
	j	.L12
.L11:
	ld	a5,-24(s0)
.L12:
	ld	a4,-32(s0)
	sd	a5,32(a4)
	ld	a5,-32(s0)
	j	.L13
.L8:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-32(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L14
	ld	a5,-24(s0)
	ld	a5,32(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,32(a5)
	j	.L15
.L14:
	ld	a5,-24(s0)
	ld	a5,24(a5)
	lw	a4,-36(s0)
	ld	a3,-24(s0)
	mv	a2,a4
	ld	a1,-32(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-24(s0)
	sd	a4,24(a5)
.L15:
	ld	a5,-24(s0)
.L13:
	mv	a0,a5
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	insertR, .-insertR
	.align	1
	.globl	pat_insert
	.type	pat_insert, @function
pat_insert:
	addi	sp,sp,-80
	sd	ra,72(sp)
	sd	s0,64(sp)
	sd	s1,56(sp)
	addi	s0,sp,80
	sd	a0,-72(s0)
	sd	a1,-80(s0)
	ld	a5,-80(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	beq	a5,zero,.L17
	ld	a5,-72(s0)
	ld	a5,8(a5)
	bne	a5,zero,.L18
.L17:
	li	a5,0
	j	.L19
.L18:
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	and	a4,a4,a5
	ld	a5,-72(s0)
	sd	a4,0(a5)
	ld	a5,-80(s0)
	sd	a5,-40(s0)
.L22:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L20
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L21
.L20:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L21:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L22
	ld	a5,-72(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a5,0(a5)
	bne	a4,a5,.L23
	sw	zero,-52(s0)
	j	.L24
.L26:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bne	a4,a5,.L25
	ld	a5,-72(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a4,8(a4)
	sd	a4,8(a5)
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	j	.L19
.L25:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L24:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L26
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-64(s0)
	sw	zero,-56(s0)
	sw	zero,-52(s0)
	ld	a5,-64(s0)
	sd	a5,-48(s0)
	j	.L27
.L30:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	bleu	a4,a5,.L28
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a4,a5
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
	j	.L29
.L28:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a4,-1
	srli	a4,a4,32
	sd	a4,0(a5)
	li	a5,1
	sw	a5,-56(s0)
.L29:
	ld	a5,-48(s0)
	addi	a5,a5,16
	sd	a5,-48(s0)
.L27:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L30
	lw	a5,-56(s0)
	sext.w	a5,a5
	bne	a5,zero,.L31
	ld	a5,-72(s0)
	ld	a5,8(a5)
	li	a2,16
	mv	a1,a5
	ld	a0,-48(s0)
	call	memmove
.L31:
	ld	a5,-72(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a0,-72(s0)
	call	free
	sd	zero,-72(s0)
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-64(s0)
	sd	a4,8(a5)
	ld	a5,-40(s0)
	j	.L19
.L23:
	li	a5,1
	sw	a5,-52(s0)
	j	.L32
.L34:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L32:
	lw	a5,-52(s0)
	sext.w	a4,a5
	li	a5,31
	bgt	a4,a5,.L33
	ld	a5,-72(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	s1,a0
	ld	a5,-40(s0)
	ld	a4,0(a5)
	lw	a5,-52(s0)
	mv	a1,a4
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	s1,a5,.L34
.L33:
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-72(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L35
	ld	a5,-80(s0)
	ld	a5,32(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,32(a5)
	j	.L36
.L35:
	ld	a5,-80(s0)
	ld	a5,24(a5)
	lw	a4,-52(s0)
	ld	a3,-80(s0)
	mv	a2,a4
	ld	a1,-72(s0)
	mv	a0,a5
	call	insertR
	mv	a4,a0
	ld	a5,-80(s0)
	sd	a4,24(a5)
.L36:
	ld	a5,-72(s0)
.L19:
	mv	a0,a5
	ld	ra,72(sp)
	ld	s0,64(sp)
	ld	s1,56(sp)
	addi	sp,sp,80
	jr	ra
	.size	pat_insert, .-pat_insert
	.align	1
	.globl	pat_remove
	.type	pat_remove, @function
pat_remove:
	addi	sp,sp,-96
	sd	ra,88(sp)
	sd	s0,80(sp)
	addi	s0,sp,96
	sd	a0,-88(s0)
	sd	a1,-96(s0)
	ld	a5,-88(s0)
	beq	a5,zero,.L38
	ld	a5,-88(s0)
	ld	a5,8(a5)
	beq	a5,zero,.L38
	ld	a5,-40(s0)
	bne	a5,zero,.L39
.L38:
	li	a5,0
	j	.L40
.L39:
	ld	a5,-96(s0)
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
.L43:
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-24(s0)
	sd	a5,-64(s0)
	ld	a5,-40(s0)
	sd	a5,-24(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L41
	ld	a5,-40(s0)
	ld	a5,32(a5)
	j	.L42
.L41:
	ld	a5,-40(s0)
	ld	a5,24(a5)
.L42:
	sd	a5,-40(s0)
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L43
	ld	a5,-40(s0)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,0(a5)
	beq	a4,a5,.L44
	li	a5,0
	j	.L40
.L44:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	mv	a4,a5
	li	a5,1
	bne	a4,a5,.L45
	ld	a5,-40(s0)
	lbu	a5,17(a5)
	bne	a5,zero,.L46
	li	a5,0
	j	.L40
.L46:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a5,0(a5)
	beq	a4,a5,.L47
	li	a5,0
	j	.L40
.L47:
	ld	a5,-24(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
.L50:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-52(s0)
	ld	a5,-32(s0)
	sd	a5,-80(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L48
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L49
.L48:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L49:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L50
	ld	a5,-80(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-24(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L51
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,32(a5)
	j	.L52
.L51:
	ld	a5,-80(s0)
	ld	a4,-40(s0)
	sd	a4,24(a5)
.L52:
	ld	a5,-64(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L53
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L54
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L55
.L54:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L55:
	ld	a4,-64(s0)
	sd	a5,32(a4)
	j	.L56
.L53:
	ld	a5,-24(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	ld	a5,-88(s0)
	ld	a5,0(a5)
	mv	a1,a5
	mv	a0,a4
	call	bit
	mv	a5,a0
	beq	a5,zero,.L57
	ld	a5,-24(s0)
	ld	a5,24(a5)
	j	.L58
.L57:
	ld	a5,-24(s0)
	ld	a5,32(a5)
.L58:
	ld	a4,-64(s0)
	sd	a5,24(a4)
.L56:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	beq	a5,zero,.L59
	ld	a5,-40(s0)
	ld	a5,8(a5)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
.L59:
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a4,-40(s0)
	ld	a5,-24(s0)
	beq	a4,a5,.L60
	ld	a5,-24(s0)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	sd	a4,0(a5)
	ld	a5,-24(s0)
	ld	a4,8(a5)
	ld	a5,-40(s0)
	sd	a4,8(a5)
	ld	a5,-24(s0)
	lbu	a4,16(a5)
	ld	a5,-40(s0)
	sb	a4,16(a5)
.L60:
	ld	a0,-24(s0)
	call	free
	li	a5,1
	j	.L40
.L45:
	sw	zero,-52(s0)
	j	.L61
.L64:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L69
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L61:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L64
	j	.L63
.L69:
	nop
.L63:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L65
	li	a5,0
	j	.L40
.L65:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a5,a5
	addiw	a5,a5,-1
	sext.w	a5,a5
	slli	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sd	a5,-72(s0)
	sw	zero,-52(s0)
	ld	a5,-72(s0)
	sd	a5,-48(s0)
	j	.L66
.L68:
	ld	a5,-88(s0)
	ld	a5,8(a5)
	ld	a4,0(a5)
	ld	a5,-40(s0)
	ld	a3,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a5,a3,a5
	ld	a5,0(a5)
	beq	a4,a5,.L67
	ld	a5,-40(s0)
	ld	a4,8(a5)
	lw	a5,-52(s0)
	slli	a5,a5,4
	add	a3,a4,a5
	ld	a5,-48(s0)
	addi	a4,a5,16
	sd	a4,-48(s0)
	li	a2,16
	mv	a1,a3
	mv	a0,a5
	call	memmove
.L67:
	lw	a5,-52(s0)
	addiw	a5,a5,1
	sw	a5,-52(s0)
.L66:
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	sext.w	a4,a5
	lw	a5,-52(s0)
	sext.w	a5,a5
	blt	a5,a4,.L68
	ld	a5,-40(s0)
	lbu	a5,16(a5)
	addiw	a5,a5,-1
	andi	a4,a5,255
	ld	a5,-40(s0)
	sb	a4,16(a5)
	ld	a5,-40(s0)
	ld	a5,8(a5)
	mv	a0,a5
	call	free
	ld	a5,-40(s0)
	ld	a4,-72(s0)
	sd	a4,8(a5)
	li	a5,1
.L40:
	mv	a0,a5
	ld	ra,88(sp)
	ld	s0,80(sp)
	addi	sp,sp,96
	jr	ra
	.size	pat_remove, .-pat_remove
	.align	1
	.globl	pat_search
	.type	pat_search, @function
pat_search:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	sd	a1,-64(s0)
	sd	zero,-24(s0)
	ld	a5,-64(s0)
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	bne	a5,zero,.L71
	li	a5,0
	j	.L72
.L71:
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L73
	ld	a5,-32(s0)
	sd	a5,-24(s0)
.L73:
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sw	a5,-36(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a5,a5
	ld	a1,-56(s0)
	mv	a0,a5
	call	bit
	mv	a5,a0
	beq	a5,zero,.L74
	ld	a5,-32(s0)
	ld	a5,32(a5)
	j	.L75
.L74:
	ld	a5,-32(s0)
	ld	a5,24(a5)
.L75:
	sd	a5,-32(s0)
	ld	a5,-32(s0)
	lbu	a5,17(a5)
	sext.w	a4,a5
	lw	a5,-36(s0)
	sext.w	a5,a5
	blt	a5,a4,.L71
	ld	a5,-32(s0)
	ld	a4,0(a5)
	ld	a5,-32(s0)
	ld	a5,8(a5)
	ld	a3,0(a5)
	ld	a5,-56(s0)
	and	a5,a3,a5
	bne	a4,a5,.L76
	ld	a5,-32(s0)
	j	.L72
.L76:
	ld	a5,-24(s0)
.L72:
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	addi	sp,sp,64
	jr	ra
	.size	pat_search, .-pat_search
	.ident	"GCC:, (GNU), 9.2.0"
